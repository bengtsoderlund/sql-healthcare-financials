# SQL and Python Financial Analysis: U.S. Healthcare Companies

## Overview
This project demonstrates how to use Python to perform structured financial analysis on four major U.S. healthcare companies, with SQL integrated for querying the data. Python is used throughout the entire workflow—including fetching data via an API, building the SQL database, executing SQL queries automatically, and visualizing the results.


## API Key and Environment Setup
This project uses the Alpha Vantage API to fetch financial data. In order to run the data fetching scripts, an API key must be provided. If no key is found, the scripts will automatically fall back on pre-fetched data stored locally in the project.

Option 1: Provide Your Own API Key
- Register for a free API key at: https://www.alphavantage.co/support/#api-key
- Create a file named `.env` in the root directory:
    - You can do this in Notepad by saving the file as ".env"
- Add the following line to the file:
    - ALPHA_VANTAGE_API_KEY=your_api_key_here
- Save the file and close Notepad

Option 2: Use Existing Data
- If no `.env` file or API key is found, the Python scripts will automatically:
    - Skip the data-fetching step
    - Use the existing data stored in the `data/` folder
- This allows you to run the project and explore the analysis without making any API calls


## Key Features
- Fetches stock prices, balance sheets, income statements, earnings, and company information via the Alpha Vantage API
- Builds an SQL database to store and structure the data
- Executes a series of SQL queries to analyze financial performance
- Outputs results to CSV files
- Visualizes key financial trends


## Companies Analyzed
- Johnson & Johnson (JNJ)
- Pfizer (PFE)
- United Healthcare (UNH)
- Medtronic (MDT)


## Data Source
- [Alpha Vantage API](https://www.alphavantage.co/)
- Note: The free API tier has a limit on the number of queries per minute and per day, which currently restricts the number of companies analyzed.
- The project is fully scalable and can easily be extended to include additional companies and sectors by adjusting the list of tickers and re-running the pipeline.


## Workflow Summary
1. Use Python to fetch financial data via API  
2. Store data in a structured SQL database  
3. Run Python code to execute and save SQL queries analyzing valuation multiples, stock volatility, profitability ratios, price reactions to earnings surprises, and monthly performance trends.
4. Visualize insights with Python charts  


## Possible Extensions
- Expand to additional companies, sectors, or international markets
- Incorporate additional financial metrics such as free cash flow, return on equity, or debt ratios
- Automate earnings call sentiment analysis to complement price reaction insights
- Integrate macroeconomic indicators (e.g., interest rates, CPI) for contextual analysis
- Build interactive dashboards using Streamlit, Dash, or Tableau for easier exploration

