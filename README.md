# SQL and Python Financial Analysis: U.S. Healthcare Companies

## Overview

This project demonstrates how Python and SQL can be combined to analyze the financial performance of major U.S. healthcare companies. It includes fetching real-world data from a public API, structuring it in a relational database, querying it with SQL, and visualizing insights with Python.

A companion Jupyter notebook walks through the full process and highlights key parts of the pipeline in a clear, readable format.

## Data and Environment Setup

Financial data is sourced from the [Alpha Vantage API](https://www.alphavantage.co/), which offers free access with usage limits (5 requests/min and 500/day). The project is designed to run with or without an API key.

**Note:** The request limit restricts the number of companies that can be fetched in a single run using the free tier. However, the pipeline itself is fully scalable and can handle any number of companies—just adjust the list of tickers and re-run the workflow.

### Option 1: Use Your Own API Key

1. Register for a free key: [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. In the root folder, create a `.env` file and add: ALPHA_VANTAGE_API_KEY=your_api_key_here
3. The scripts will detect the key and fetch up-to-date financial data.

### Option 2: Use Pre-Fetched Data

If no `.env` file or key is found:
- The scripts will skip the API requests
- Pre-fetched data in the `data/` folder will be used instead
- All SQL queries and visualizations will still work

## Project Workflow

- **Fetch Financial Data**  
Retrieve stock prices, balance sheets, income statements, earnings, and company overviews via the Alpha Vantage API (or use local fallback data).

- **Build a SQL Database**  
Load the fetched data into a structured SQLite database to enable efficient querying.

- **Run Analytical SQL Queries**  
Use SQL to examine valuation multiples, profitability ratios, stock volatility, post-earnings drift, earnings surprises, and monthly performance trends.

- **Export Results**  
Save the outputs of all queries as `.csv` files for transparency and reuse.

- **Generate Visualizations**  
Create data visualizations using `matplotlib` and `seaborn`, including charts for earnings reactions, valuation metrics, and more.

- **Interactive Notebook**  
A Jupyter notebook provides a guided, end-to-end walkthrough of the pipeline, combining data, SQL, and visualization in one place.

## Companies Analyzed

- Johnson & Johnson (JNJ)  
- Pfizer (PFE)  
- United Healthcare (UNH)  
- Medtronic (MDT)

## Possible Extensions

- Add more companies, industries, or countries  
- Integrate additional financial metrics (e.g., free cash flow, debt ratios)  
- Automate sentiment analysis of earnings calls  
- Include macroeconomic indicators like CPI or interest rates  
- Build interactive dashboards using Streamlit, Dash, or Tableau


