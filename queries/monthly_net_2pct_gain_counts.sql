-- Calculate the number of >2% open-to-close gain days per month and the number  
-- of <-2% open-to-close loss days per stock. Also includes the net number of  
-- such days, the average daily return, and the total number of trading days  
-- per month. Covers the most recent 36 full calendar months.

WITH net_gain AS(
	SELECT
		symbol,
		date,
		strftime('%Y-%m', date) AS month,
		open,
		close,
		((close-open)/open) AS daily_return_pct,
		((close-open)/open) > 0.02 AS gain_over_2pct,
		((close-open)/open) < -0.02 AS loss_over_2pct
	FROM stock_prices
	WHERE date >= DATE('now', 'start of month', '-35 months')
)
SELECT
	n.symbol,
	n.month,
	SUM(gain_over_2pct) AS nr_2pct_gains,
	SUM(loss_over_2pct) AS nr_2pct_losses,
	SUM(gain_over_2pct) - SUM(loss_over_2pct) AS nr_net_gains,
	AVG(daily_return_pct) AS avg_return,
	COUNT(*) AS days_in_month,
	c.Name AS company_name
FROM net_gain AS n
JOIN company_overviews AS c ON n.symbol = c.symbol
GROUP BY n.symbol, n.month