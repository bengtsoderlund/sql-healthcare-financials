-- Calculate the average monthly intraday volatility (% change between high and low relative to open)
-- for each stock over the last 6 calendar months. Includes count of trading days per month.

SELECT
    symbol,
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(((high - low) / open ) * 100), 2) AS avg_volatility_pct,
    COUNT(*) AS days_in_month
FROM stock_prices
WHERE date >= DATE('now', 'start of month', '-5 months')
GROUP BY symbol, month
ORDER BY symbol;