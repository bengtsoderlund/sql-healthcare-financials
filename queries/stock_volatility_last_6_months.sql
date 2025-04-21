-- Calculate the average daily return (% change from open to close) for each stock
-- over the last full 6 calendar months. Results include the number of trading days 
-- per month. Daily returns are expressed as percentages and rounded to two decimals.

SELECT
    s.symbol,
    c.Name AS company_name,
    strftime('%Y-%m', s.date) AS month,
    ROUND(AVG(100.0 * (s.close - s.open) / s.open),2) AS avg_daily_return,
    COUNT(*) AS trading_days
FROM
    stock_prices AS s
JOIN
    company_overviews AS c ON s.symbol = c.symbol
WHERE
    date >= DATE('now', 'start of month', '-6 months') AND date < DATE('now', 'start of month')
GROUP BY
    s.symbol, month
ORDER BY
    s.symbol, month