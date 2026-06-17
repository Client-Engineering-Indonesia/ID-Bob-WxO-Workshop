"""
Yahoo Finance Tool for watsonx Orchestrate
Fetches stock prices, volume, historical trends, and market cap for multiple tickers
"""

import yfinance as yf
from datetime import datetime
from typing import List, Dict, Any
import logging
import json
import math
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def get_formatted_stock_data(tickers: str, period: str = "1mo") -> str:
    """
    Fetch comprehensive stock data for multiple tickers with formatted output.
    
    Args:
        tickers: Comma-separated list of stock ticker symbols (e.g., "AAPL,GOOGL,MSFT")
        period: Time period for historical data (default: "1mo" for 30 days)
    
    Returns:
        Formatted string with stock data including current price, volume, market cap, 
        30-day trends, P/E ratio, and sector information
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
        results = {}
        
        for ticker in ticker_list:
            logger.info(f"Fetching data for {ticker}")
            stock = yf.Ticker(ticker)
            
            # Get current info
            info = stock.info
            
            # Get historical data
            hist = stock.history(period=period)
            
            if hist.empty:
                logger.warning(f"No historical data found for {ticker}")
                results[ticker] = {
                    "error": f"No data available for ticker {ticker}",
                    "status": "failed"
                }
                continue
            
            # Calculate metrics
            current_price = hist['Close'].iloc[-1]
            volume = hist['Volume'].iloc[-1]
            
            # Historical trends
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[0] if len(hist) > 1 else 0
            price_change_pct = (price_change / hist['Close'].iloc[0] * 100) if len(hist) > 1 and hist['Close'].iloc[0] != 0 else 0
            
            avg_volume = hist['Volume'].mean()
            high_30d = hist['High'].max()
            low_30d = hist['Low'].min()
            
            # Compile results with NaN handling
            results[ticker] = {
                "status": "success",
                "ticker": ticker,
                "company_name": info.get('longName', 'N/A'),
                "current_data": {
                    "price": round(current_price, 2) if current_price and not math.isnan(current_price) else None,
                    "volume": int(volume) if volume and not math.isnan(volume) else None,
                    "market_cap": info.get('marketCap', 'N/A'),
                    "currency": info.get('currency', 'USD')
                },
                "historical_trends_30d": {
                    "price_change": round(price_change, 2) if not math.isnan(price_change) else 0,
                    "price_change_percentage": round(price_change_pct, 2) if not math.isnan(price_change_pct) else 0,
                    "high": round(high_30d, 2) if not math.isnan(high_30d) else None,
                    "low": round(low_30d, 2) if not math.isnan(low_30d) else None,
                    "average_volume": int(avg_volume) if not math.isnan(avg_volume) else 0
                },
                "additional_info": {
                    "sector": info.get('sector', 'N/A'),
                    "industry": info.get('industry', 'N/A'),
                    "pe_ratio": info.get('trailingPE', 'N/A'),
                    "dividend_yield": info.get('dividendYield', 'N/A')
                },
                "timestamp": datetime.now().isoformat()
            }
        
        # Format output
        output = []
        output.append(f"📊 Stock Data Analysis")
        output.append(f"Processed {len(ticker_list)} ticker(s)\n")
        
        for ticker, ticker_data in results.items():
            if ticker_data.get("status") == "success":
                output.append(f"{'='*60}")
                output.append(f"🏢 {ticker_data['company_name']} ({ticker})")
                output.append(f"{'='*60}")
                
                cd = ticker_data["current_data"]
                output.append(f"\n💰 Current Price: ${cd['price']} {cd['currency']}")
                output.append(f"📈 Market Cap: {cd['market_cap']:,}" if isinstance(cd['market_cap'], (int, float)) else f"📈 Market Cap: {cd['market_cap']}")
                output.append(f"📊 Volume: {cd['volume']:,}" if cd['volume'] else "📊 Volume: N/A")
                
                ht = ticker_data["historical_trends_30d"]
                output.append(f"\n📅 30-Day Performance:")
                output.append(f"  • Change: ${ht['price_change']} ({ht['price_change_percentage']:+.2f}%)")
                output.append(f"  • High: ${ht['high']}")
                output.append(f"  • Low: ${ht['low']}")
                output.append(f"  • Avg Volume: {ht['average_volume']:,}")
                
                ai = ticker_data["additional_info"]
                output.append(f"\nℹ️  Additional Info:")
                output.append(f"  • Sector: {ai['sector']}")
                output.append(f"  • Industry: {ai['industry']}")
                output.append(f"  • P/E Ratio: {ai['pe_ratio']}")
                output.append(f"\n")
            else:
                output.append(f"❌ {ticker}: {ticker_data.get('error', 'Unknown error')}\n")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return f"Error: {str(e)}"


@tool
def get_stock_comparison(tickers: str) -> str:
    """
    Compare multiple stocks side by side with key metrics.
    
    Args:
        tickers: Comma-separated list of stock ticker symbols to compare (e.g., "AAPL,GOOGL,MSFT")
    
    Returns:
        JSON string with comparison data including price, market cap, 30-day change, and sector
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
        results = {}
        
        for ticker in ticker_list:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1mo")
            
            if hist.empty:
                continue
            
            current_price = hist['Close'].iloc[-1]
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[0] if len(hist) > 1 else 0
            price_change_pct = (price_change / hist['Close'].iloc[0] * 100) if len(hist) > 1 and hist['Close'].iloc[0] != 0 else 0
            
            results[ticker] = {
                "ticker": ticker,
                "company": info.get('longName', 'N/A'),
                "price": round(current_price, 2) if not math.isnan(current_price) else None,
                "market_cap": info.get('marketCap', 'N/A'),
                "30d_change_pct": round(price_change_pct, 2) if not math.isnan(price_change_pct) else 0,
                "sector": info.get('sector', 'N/A')
            }
        
        comparison = {
            "comparison_date": datetime.now().isoformat(),
            "tickers": ticker_list,
            "summary": list(results.values())
        }
        
        return json.dumps(comparison, indent=2)
        
    except Exception as e:
        logger.error(f"Error comparing stocks: {str(e)}")
        return json.dumps({"error": str(e)}, indent=2)


# Example usage
if __name__ == "__main__":
    # Test the tools
    print("Testing Yahoo Finance Tools...")
    print("\n" + "="*80 + "\n")
    
    result = get_formatted_stock_data("AAPL,GOOGL,MSFT")
    print(result)
    
    print("\n" + "="*80 + "\n")
    print("Comparison View:")
    comparison = get_stock_comparison("AAPL,GOOGL,MSFT")
    print(comparison)

# Made with Bob
