-- Calculate the number of >2% open-to-close gain days per month for each stock,
-- over the last 36 full calendar months. Includes total trading days per month.

WITH gain AS(
	SELECT
		symbol,
		date,
		strftime('%Y-%m', date) AS month,
		open,
		close,
		close-open/open AS daily_return_pct,
		((close-open)/open) > 0.02 AS gain_over_2pct 
	FROM stock_prices
	WHERE date >= DATE('now', 'start of month', '-35 months')
)
SELECT
	symbol,
	month,
	SUM(gain_over_2pct) as nr_2pct_gains,
	COUNT(*) AS days_in_month
FROM gain
GROUP BY symbol, month