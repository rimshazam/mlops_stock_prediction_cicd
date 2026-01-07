from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'database'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_NAME', 'stocks'),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    ticker = data.get('ticker', '').upper()
    
    if not ticker:
        return jsonify({'error': 'Ticker symbol required'}), 400
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Get last 3 days of prices
            sql = """
                SELECT price, date 
                FROM stock_prices 
                WHERE ticker = %s 
                ORDER BY date DESC 
                LIMIT 3
            """
            cursor.execute(sql, (ticker,))
            results = cursor.fetchall()
            
            if len(results) < 3:
                return jsonify({
                    'error': f'Insufficient data for {ticker}. Need at least 3 days of historical data.'
                }), 404
            
            # Calculate moving average (simple rule-based prediction)
            prices = [float(row['price']) for row in results]
            moving_avg = sum(prices) / len(prices)
            
            # Predicted price for tomorrow
            prediction = round(moving_avg, 2)
            
            return jsonify({
                'ticker': ticker,
                'predicted_price': prediction,
                'last_3_prices': prices,
                'prediction_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                'method': 'Moving Average (3-day)'
            }), 200
            
    except pymysql.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/stocks', methods=['GET'])
def get_stocks():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker"
            cursor.execute(sql)
            results = cursor.fetchall()
            tickers = [row['ticker'] for row in results]
            return jsonify({'tickers': tickers}), 200
    except pymysql.Error as e:
        return jsonify({'error': f'Database errorr: {str(e)}'}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)