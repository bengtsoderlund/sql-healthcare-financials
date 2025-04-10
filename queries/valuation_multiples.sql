-- Calculates common valuation multiples (P/E, P/S, P/B) using the first available
-- closing price after each fiscal year end, combined with fundamentals from the
-- corresponding annual income statements and balance sheets. Useful for comparing
-- relative valuation across companies and time.

WITH dated_prices AS (
    SELECT
        s.symbol,
	    s.date,
	    s.close,
	    i.netIncome,
	    i.totalRevenue,
	    b.totalShareholderEquity,
	    b.commonStockSharesOutstanding,
	    ROW_NUMBER() OVER (PARTITION BY s.symbol, i.fiscal_date ORDER BY s.date) AS rn
    FROM stock_prices AS s
    JOIN income_statements AS i ON s.symbol=i.symbol AND s.date >= i.fiscal_date
    JOIN balance_sheets AS b ON s.symbol=b.symbol AND i.fiscal_date = b.fiscal_date
    WHERE i.report_type == 'annual' AND b.report_type == 'annual'
)
SELECT
    symbol,
	date AS price_date,
	netIncome,
	totalRevenue,
	totalShareholderEquity,
	commonStockSharesOutstanding,
	ROUND(close / (netIncome * 1.0 / commonStockSharesOutstanding),2) AS PE,
	ROUND(close / (totalRevenue * 1.0 / commonStockSharesOutstanding),2) AS PS,
	ROUND(close / (totalShareholderEquity * 1.0 / commonStockSharesOutstanding),2) AS PB
FROM dated_prices
WHERE rn = 1