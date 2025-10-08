const API_URL = 'http://localhost:5000';

document.getElementById('predictBtn').addEventListener('click', predictPrice);
document.getElementById('tickerInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') predictPrice();
});

async function predictPrice() {
    const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const loadingDiv = document.getElementById('loading');

    if (!ticker) {
        showError('Please enter a stock ticker symbol');
        return;
    }

    // Hide previous results
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ticker: ticker })
        });

        const data = await response.json();
        loadingDiv.classList.add('hidden');

        if (response.ok) {
            showResult(data);
        } else {
            showError(data.error || 'Failed to get prediction');
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        showError('Connection error. Make sure the backend server is running.');
    }
}

function showResult(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <h3>Prediction for ${data.ticker}</h3>
        <div class="predicted-price">$${data.predicted_price}</div>
        <div class="price-info">
            <p><strong>Prediction Date:</strong> ${data.prediction_date}</p>
            <p><strong>Method:</strong> ${data.method}</p>
            <p><strong>Last 3 Prices:</strong> $${data.last_3_prices.join(', $')}</p>
        </div>
    `;
    resultDiv.classList.remove('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}