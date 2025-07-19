import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
from mcp_client import MCPClient
from sentiment_analyzer import SentimentAnalyzer

class DataAggregator:
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.sentiment_analyzer = SentimentAnalyzer()
        
    async def aggregate_market_data(self, symbols: List[str]) -> Dict[str, Any]:
        market_data = {}
        
        for symbol in symbols:
            stock_data = await self.mcp_client.get_stock_data(symbol)
            market_data[symbol] = {
                "stock_info": stock_data,
                "timestamp": datetime.now().isoformat()
            }
            
        return market_data
    
    async def aggregate_news_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        news_sentiment = {}
        
        market_news = await self.mcp_client.get_market_news(limit=20)
        
        for symbol in symbols:
            symbol_news = [
                news for news in market_news 
                if symbol.lower() in news.get("title", "").lower() or 
                   symbol.lower() in news.get("summary", "").lower()
            ]
            
            sentiment_scores = []
            for news in symbol_news:
                text = f"{news.get('title', '')} {news.get('summary', '')}"
                sentiment = self.sentiment_analyzer.analyze_text(text)
                sentiment_scores.append(sentiment)
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            news_sentiment[symbol] = {
                "news_count": len(symbol_news),
                "avg_sentiment": avg_sentiment,
                "news_items": symbol_news[:5],
                "timestamp": datetime.now().isoformat()
            }
            
        return news_sentiment
    
    async def aggregate_social_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        social_sentiment = {}
        
        for symbol in symbols:
            tweets = await self.mcp_client.get_twitter_sentiment(f"${symbol}", count=50)
            
            sentiment_scores = []
            for tweet in tweets:
                if isinstance(tweet, dict) and "text" in tweet:
                    sentiment = self.sentiment_analyzer.analyze_text(tweet["text"])
                    sentiment_scores.append(sentiment)
            
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            social_sentiment[symbol] = {
                "tweet_count": len(tweets),
                "avg_sentiment": avg_sentiment,
                "sample_tweets": tweets[:3],
                "timestamp": datetime.now().isoformat()
            }
            
        return social_sentiment
    
    async def get_technical_analysis(self, symbols: List[str]) -> Dict[str, Any]:
        technical_data = {}
        
        for symbol in symbols:
            chart_path = await self.mcp_client.get_chart_screenshot(symbol)
            technical_data[symbol] = {
                "chart_path": chart_path,
                "timestamp": datetime.now().isoformat()
            }
            
        return technical_data
    
    async def generate_comprehensive_report(self, symbols: List[str]) -> Dict[str, Any]:
        market_data, news_sentiment, social_sentiment, technical_data = await asyncio.gather(
            self.aggregate_market_data(symbols),
            self.aggregate_news_sentiment(symbols),
            self.aggregate_social_sentiment(symbols),
            self.get_technical_analysis(symbols)
        )
        
        return {
            "market_data": market_data,
            "news_sentiment": news_sentiment,
            "social_sentiment": social_sentiment,
            "technical_analysis": technical_data,
            "generated_at": datetime.now().isoformat()
        }
