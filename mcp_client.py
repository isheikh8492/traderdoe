import asyncio
import json
from typing import Dict, List, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self, server_configs: Dict[str, Dict[str, Any]]):
        self.server_configs = server_configs
        self.sessions = {}
        
    async def connect_to_servers(self):
        for server_name, config in self.server_configs.items():
            try:
                server_params = StdioServerParameters(
                    command=config["command"],
                    args=config["args"]
                )
                
                stdio_transport = await stdio_client(server_params)
                session = ClientSession(stdio_transport[0], stdio_transport[1])
                await session.initialize()
                
                self.sessions[server_name] = session
                print(f"Connected to {server_name} MCP server")
                
            except Exception as e:
                print(f"Failed to connect to {server_name}: {e}")
    
    async def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        if "yahoo_finance" not in self.sessions:
            return {"error": "Yahoo Finance server not connected"}
            
        try:
            session = self.sessions["yahoo_finance"]
            result = await session.call_tool("get_stock_info", {"symbol": symbol})
            return result.content[0].text if result.content else {}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_market_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        if "yahoo_finance" not in self.sessions:
            return [{"error": "Yahoo Finance server not connected"}]
            
        try:
            session = self.sessions["yahoo_finance"]
            result = await session.call_tool("get_market_news", {"limit": limit})
            return json.loads(result.content[0].text) if result.content else []
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_twitter_sentiment(self, query: str, count: int = 50) -> List[Dict[str, Any]]:
        if "twitter" not in self.sessions:
            return [{"error": "Twitter server not connected"}]
            
        try:
            session = self.sessions["twitter"]
            result = await session.call_tool("search_tweets", {
                "query": query,
                "count": count
            })
            return json.loads(result.content[0].text) if result.content else []
        except Exception as e:
            return [{"error": str(e)}]
    
    async def get_chart_screenshot(self, symbol: str, timeframe: str = "1D") -> str:
        if "tradingview" not in self.sessions:
            return "TradingView server not connected"
            
        try:
            session = self.sessions["tradingview"]
            result = await session.call_tool("capture_chart", {
                "symbol": symbol,
                "timeframe": timeframe
            })
            return result.content[0].text if result.content else ""
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def close_connections(self):
        for session in self.sessions.values():
            await session.close()
        self.sessions.clear()