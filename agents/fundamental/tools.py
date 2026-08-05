import yfinance as yf
import json


def get_company_info(ticker: str) -> str:
    """Fetches company profile info, sector, industry, and business summary.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker)  # stock is an object of ticker class
        info = stock.info 

        profile = {
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "summary": info.get("longBusinessSummary"),
            "market_cap": info.get("marketCap")
        }

        return json.dumps(profile, indent=2) # it converts the profile dictionary into a JSON-formatted string with an indentation of 2 spaces for better readability. 

    except Exception as e:
        return f"Error fetching company info for {ticker}: {str(e)}"


def get_income_statement(ticker: str) -> str:
    """Fetches the company's recent annual income statements.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.financials # fetches the annual income statement data and it's return type is DataFrame, which is a 2-dimensional labeled data structure with columns of potentially different types.

        df.index = df.index.str.strip() # gets rid of any leading or trailing whitespace characters from the index labels of the DataFrame.

        keys = ["Total Revenue", "Net Income", "Diluted EPS"]

        data = {}

        for key in keys:
            if key in df.index:
                values = df.loc[key].round(2).to_dict() # selects the row corresponding to the key, rounds the values to 2 decimal places, and converts it to a dictionary.
                data[key] = {
                    str(date)[:10]: val
                    for date, val in values.items()
                }

        return json.dumps(data, indent=2, default=str)

    except Exception as e:
        return f"Error fetching income statement for {ticker}: {str(e)}"


def get_balance_sheet(ticker: str) -> str:
    """Fetches the company's recent annual balance sheets.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.balance_sheet

        df.index = df.index.str.strip()

        keys = [
            "Total Assets",
            "Total Liabilities Net Minority Interest",
            "Total Debt",
            "Cash Cash Equivalents And Short Term Investments"
        ]

        # use fallback labels if Yahoo Finance uses different labels for certain balance sheet items 
        fallbacks = {
            "Total Liabilities Net Minority Interest": [
                "Total Liabilities"
            ],
            "Cash Cash Equivalents And Short Term Investments": [
                "Cash And Short Term Investments",
                "Cash"
            ]
        }

        data = {}

        for key in keys:
            matched_key = key

            if key not in df.index and key in fallbacks:
                for fallback in fallbacks[key]:
                    if fallback in df.index:
                        matched_key = fallback
                        break

            if matched_key in df.index:
                values = df.loc[matched_key].round(2).to_dict()

                data[key] = {
                    str(date)[:10]: val
                    for date, val in values.items()
                }

        return json.dumps(data, indent=2, default=str)

    except Exception as e:
        return f"Error fetching balance sheet for {ticker}: {str(e)}"


def get_financial_ratios(ticker: str) -> str:
    """Fetches valuation metrics and efficiency ratios.

    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        ratios = {
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "ps_ratio": info.get("priceToSalesTrailing12Months"),
            "pb_ratio": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "operating_margin": info.get("operatingMargins"),
            "profit_margin": info.get("profitMargins"),
            "debt_to_equity": info.get("debtToEquity")
        }

        return json.dumps(ratios, indent=2, default=str)

    except Exception as e:
        return f"Error fetching financial ratios for {ticker}: {str(e)}"