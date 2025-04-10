-- Calculate annual gross_margin, net_margin, return_on_assets, and return_on_equity
-- for each stock, using joined income statements and balance sheets.

SELECT
    i.symbol,
	i.fiscal_date,
	ROUND( 100.0 * (i.totalRevenue-i.costOfRevenue)/i.totalRevenue, 1) AS gross_margin,
	ROUND( 100.0 * i.netIncome/i.totalRevenue, 1) AS net_margin,
	ROUND( 100.0 * i.netIncome/b.totalAssets, 1) AS return_on_assets,
	ROUND( 100.0 * i.netIncome/b.totalShareholderEquity, 1) AS return_on_equity
	
FROM
    income_statements AS i
JOIN
    balance_sheets AS b ON i.symbol=b.symbol AND i.fiscal_date=b.fiscal_date
WHERE
    i.report_type = 'annual' AND b.report_type = 'annual'