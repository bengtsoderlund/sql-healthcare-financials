-- Measures post-earnings drift by calculating stock returns from day 6 to day 
-- 20 following the earnings report date for the last 20 quarters. Results are 
-- grouped by surprise direction (positive vs. negative) to identify whether 
-- stocks tend to continue drifting in the direction of the earnings surprise 
-- after the initial reaction.

WITH stock_prices_rows AS (
    SELECT
	    symbol,
		date,
		close,
		ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date) AS stock_rn
	FROM
	    stock_prices
),
earnings_rows AS (
    SELECT
	    e.symbol,
		e.fiscal_quarter,
		e.reported_date,
		e.surprise_pct,
		s.stock_rn AS earnings_rn 
	FROM
	    quarterly_earnings AS e
	JOIN
	    stock_prices_rows AS s ON e.symbol=s.symbol AND e.reported_date=s.date		
)
SELECT
    e.symbol,
    c.Name AS name,
	e.fiscal_quarter,
	e.reported_date,
	ROUND(e.surprise_pct, 2) AS surprise_pct,
	(surprise_pct > 0) AS is_positive_surprise,
	s6.close AS day_6_price,
	s20.close AS day_20_price,
	ROUND(100*(s20.close-s6.close)/s6.close,2) AS post_earnings_drift_pct
FROM
    earnings_rows AS e
JOIN
    stock_prices_rows AS s6 ON e.symbol=s6.symbol AND e.earnings_rn+6=s6.stock_rn
JOIN
    stock_prices_rows AS s20 ON e.symbol=s20.symbol AND e.earnings_rn+20=s20.stock_rn
JOIN
   company_overviews AS c ON e.symbol=c.symbol
WHERE
    e.fiscal_quarter > DATE('now', 'start of month', '-60 months')