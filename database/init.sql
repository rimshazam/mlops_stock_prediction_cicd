CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

CREATE TABLE IF NOT EXISTS stock_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ticker_date (ticker, date)
);

-- Insert sample data for testing
INSERT INTO stock_prices (ticker, price, date) VALUES
('AAPL', 178.50, '2025-10-01'),
('AAPL', 180.25, '2025-10-02'),
('AAPL', 179.75, '2025-10-03'),
('AAPL', 181.00, '2025-10-04'),

('GOOGL', 140.30, '2025-10-01'),
('GOOGL', 142.15, '2025-10-02'),
('GOOGL', 141.80, '2025-10-03'),
('GOOGL', 143.25, '2025-10-04'),

('MSFT', 375.20, '2025-10-01'),
('MSFT', 378.50, '2025-10-02'),
('MSFT', 377.90, '2025-10-03'),
('MSFT', 380.15, '2025-10-04'),

('TSLA', 245.60, '2025-10-01'),
('TSLA', 248.30, '2025-10-02'),
('TSLA', 247.85, '2025-10-03'),
('TSLA', 250.10, '2025-10-04');