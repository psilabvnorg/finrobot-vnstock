"""
VNStock Utils - Vietnamese Stock Market Data Integration
Provides Vietnamese stock market data using vnstock3 library
"""

from vnstock import Vnstock
from typing import Annotated, Optional
from pandas import DataFrame
from datetime import datetime, timedelta

from ..utils import save_output, SavePathType


class VNStockUtils:
    """
    Vietnamese Stock Market Data Utilities
    
    Provides access to Vietnamese stock market data including:
    - Historical price data
    - Financial statements (Balance Sheet, Income Statement, Cash Flow)
    - Financial ratios
    - Company information
    
    Data sources: VCI, TCBS, MSN
    """

    def get_stock_data(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        start_date: Annotated[str, "Start date YYYY-MM-DD"] = None,
        end_date: Annotated[str, "End date YYYY-MM-DD"] = None,
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        Retrieve historical stock price data for Vietnamese ticker symbol.
        
        Returns DataFrame with columns: time, open, high, low, close, volume
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            stock_data = stock.quote.history(start=start_date, end=end_date)
            save_output(stock_data, f"Stock data for {symbol}", save_path)
            return stock_data
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return DataFrame()

    def get_company_info(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """
        Fetch basic company information for Vietnamese stock.
        
        Note: Vietnamese market has limited public company info compared to US markets.
        Returns basic ticker information.
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            # Get recent price data to show company is active
            recent_data = stock.quote.history(
                start=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                end=datetime.now().strftime("%Y-%m-%d")
            )
            
            company_info = {
                "Ticker Symbol": symbol,
                "Market": "Vietnam (HOSE/HNX/UPCOM)",
                "Currency": "VND",
                "Latest Close": recent_data['close'].iloc[-1] if len(recent_data) > 0 else "N/A",
                "Latest Volume": recent_data['volume'].iloc[-1] if len(recent_data) > 0 else "N/A",
                "Note": "Use finance methods for detailed financial data"
            }
            
            company_info_df = DataFrame([company_info])
            if save_path:
                company_info_df.to_csv(save_path)
                print(f"Company info for {symbol} saved to {save_path}")
            return company_info_df
        except Exception as e:
            print(f"Error fetching company info for {symbol}: {e}")
            return DataFrame()

    def get_balance_sheet(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        period: Annotated[str, "'year' for annual, 'quarter' for quarterly"] = "year",
        lang: Annotated[str, "'vi' for Vietnamese, 'en' for English"] = "vi",
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """
        Fetch balance sheet (Bảng cân đối kế toán) for Vietnamese stock.
        
        Args:
            period: 'year' for annual data, 'quarter' for quarterly data
            lang: 'vi' for Vietnamese column names, 'en' for English
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            balance_sheet = stock.finance.balance_sheet(
                period=period, 
                lang=lang, 
                dropna=True
            )
            if save_path:
                balance_sheet.to_csv(save_path)
                print(f"Balance sheet for {symbol} saved to {save_path}")
            return balance_sheet
        except Exception as e:
            print(f"Error fetching balance sheet for {symbol}: {e}")
            return DataFrame()

    def get_income_stmt(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        period: Annotated[str, "'year' for annual, 'quarter' for quarterly"] = "year",
        lang: Annotated[str, "'vi' for Vietnamese, 'en' for English"] = "vi",
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """
        Fetch income statement (Kết quả hoạt động kinh doanh) for Vietnamese stock.
        
        Args:
            period: 'year' for annual data, 'quarter' for quarterly data
            lang: 'vi' for Vietnamese column names, 'en' for English
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            income_stmt = stock.finance.income_statement(
                period=period,
                lang=lang,
                dropna=True
            )
            if save_path:
                income_stmt.to_csv(save_path)
                print(f"Income statement for {symbol} saved to {save_path}")
            return income_stmt
        except Exception as e:
            print(f"Error fetching income statement for {symbol}: {e}")
            return DataFrame()

    def get_cash_flow(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        period: Annotated[str, "'year' for annual, 'quarter' for quarterly"] = "year",
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """
        Fetch cash flow statement (Lưu chuyển tiền tệ) for Vietnamese stock.
        
        Args:
            period: 'year' for annual data, 'quarter' for quarterly data
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            cash_flow = stock.finance.cash_flow(
                period=period,
                dropna=True
            )
            if save_path:
                cash_flow.to_csv(save_path)
                print(f"Cash flow for {symbol} saved to {save_path}")
            return cash_flow
        except Exception as e:
            print(f"Error fetching cash flow for {symbol}: {e}")
            return DataFrame()

    def get_financial_ratios(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        period: Annotated[str, "'year' for annual, 'quarter' for quarterly"] = "year",
        lang: Annotated[str, "'vi' for Vietnamese, 'en' for English"] = "vi",
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """
        Fetch financial ratios (Chỉ số tài chính) for Vietnamese stock.
        
        Includes valuation ratios like P/E, P/B, EPS, BVPS, etc.
        
        Args:
            period: 'year' for annual data, 'quarter' for quarterly data
            lang: 'vi' for Vietnamese column names, 'en' for English
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            ratios = stock.finance.ratio(
                period=period,
                lang=lang,
                dropna=True
            )
            if save_path:
                ratios.to_csv(save_path)
                print(f"Financial ratios for {symbol} saved to {save_path}")
            return ratios
        except Exception as e:
            print(f"Error fetching financial ratios for {symbol}: {e}")
            return DataFrame()

    # ============================================================================
    # STUB METHODS - Features not available in Vietnamese market
    # ============================================================================
    
    def get_analyst_recommendations(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
    ) -> tuple:
        """
        Analyst recommendations not available for Vietnamese market.
        
        Vietnamese brokerage firms (SSI, VPS, VCBS) publish reports but 
        no centralized API exists for programmatic access.
        
        Returns: ("N/A", None)
        """
        print(f"Analyst recommendations not available for Vietnamese stock {symbol}")
        return ("N/A", None)

    def get_target_price(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        date: Annotated[str, "Date YYYY-MM-DD"] = None,
    ) -> str:
        """
        Target prices not available for Vietnamese market via API.
        
        Vietnamese market does not have centralized target price databases.
        Individual brokers publish target prices in PDF reports.
        
        Returns: "N/A"
        """
        print(f"Target price not available for Vietnamese stock {symbol}")
        return "N/A"

    def get_stock_dividends(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """
        Dividend data - limited availability in vnstock.
        
        Note: Vietnamese dividend data may need to be scraped from 
        company announcements or HOSE/HNX websites.
        
        Returns: Empty DataFrame
        """
        print(f"Dividend data not directly available in vnstock for {symbol}")
        print(f"Check company announcements on HOSE/HNX or company website")
        return DataFrame()

    def get_stock_info(
        symbol: Annotated[str, "Vietnamese ticker symbol (e.g., VPB, VNM, HPG)"],
        source: Annotated[str, "Data source: VCI, TCBS, or MSN"] = "VCI",
    ) -> dict:
        """
        Get stock information as dictionary.
        
        Limited data compared to US markets (yfinance).
        Returns basic information available from recent trading data.
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=source)
            recent_data = stock.quote.history(
                start=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                end=datetime.now().strftime("%Y-%m-%d")
            )
            
            if len(recent_data) == 0:
                return {
                    "symbol": symbol,
                    "currency": "VND",
                    "shortName": symbol,
                    "error": "No recent data available"
                }
            
            latest = recent_data.iloc[-1]
            
            return {
                "symbol": symbol,
                "shortName": symbol,
                "currency": "VND",
                "currentPrice": float(latest['close']),
                "volume": int(latest['volume']),
                "open": float(latest['open']),
                "high": float(latest['high']),
                "low": float(latest['low']),
                "previousClose": float(recent_data.iloc[-2]['close']) if len(recent_data) > 1 else float(latest['close']),
                "marketCap": "N/A - Use financial_ratios() for market data",
                "sector": "N/A - Check HOSE/HNX listing",
                "industry": "N/A - Check HOSE/HNX listing",
            }
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            return {
                "symbol": symbol,
                "currency": "VND",
                "error": str(e)
            }


# Example usage
if __name__ == "__main__":
    print("Testing VNStock Utils...")
    
    # Test historical data
    print("\n1. Historical Stock Data:")
    data = VNStockUtils.get_stock_data("VPB", "VCI", "2024-01-01", "2024-12-31")
    print(data.head())
    
    # Test balance sheet
    print("\n2. Balance Sheet (Vietnamese):")
    bs = VNStockUtils.get_balance_sheet("VPB", "VCI", period="year", lang="vi")
    print(bs.head())
    
    # Test income statement
    print("\n3. Income Statement (English):")
    income = VNStockUtils.get_income_stmt("VPB", "VCI", period="year", lang="en")
    print(income.head())
    
    # Test financial ratios
    print("\n4. Financial Ratios:")
    ratios = VNStockUtils.get_financial_ratios("VPB", "VCI", period="year", lang="vi")
    print(ratios.head())
    
    # Test company info
    print("\n5. Company Info:")
    info = VNStockUtils.get_company_info("VPB", "VCI")
    print(info)
    
    print("\n✅ VNStock Utils integration complete!")
