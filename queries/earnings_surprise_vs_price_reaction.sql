-- Computes earnings surprise and the corresponding 5-day stock return  
-- for all quarterly reports since 2018.  
-- Surprise is calculated as the percent difference between reported and estimated EPS.  
-- Stock return reflects the percentage change in closing price from the report date  
-- to five trading days later.

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
	e.fiscal_quarter,
	e.reported_date,
	ROUND(e.surprise_pct, 2) AS surprise_pct,
	s0.close AS day_0_price,
	s5.close AS day_5_price,
	ROUND(100*(s5.close-s0.close)/s0.close,2) AS price_change_5d_pct
FROM
    earnings_rows AS e
JOIN
    stock_prices_rows AS s0 ON e.symbol=s0.symbol AND e.earnings_rn=s0.stock_rn
JOIN
    stock_prices_rows AS s5 ON e.symbol=s5.symbol AND e.earnings_rn+5=s5.stock_rn
WHERE
    e.fiscal_quarter > '2018-01-01'
	