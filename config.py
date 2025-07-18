import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    MCP_SERVERS = {
        "yahoo_finance": {
            "command": "uv",
            "args": ["--directory", "/path/to/yahoo-finance-mcp", "run", "yahoo-finance-mcp"]
        },
        "twitter": {
            "command": "node",
            "args": ["/path/to/twitter-mcp/index.js"]
        },
        "tradingview": {
            "command": "python",
            "args": ["/path/to/tradingview-mcp/server.py"]
        }
    }
    
    TRADING_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "SPY", "QQQ"]
    
    SENTIMENT_KEYWORDS = [
        "bullish", "bearish", "buy", "sell", "pump", "dump", 
        "moon", "crash", "breakout", "support", "resistance"
    ]