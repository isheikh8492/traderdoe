import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from anthropic import Anthropic
from config import Config

class AIAnalyzer:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        
    async def analyze_trading_data(self, comprehensive_report: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_analysis_prompt(comprehensive_report)
        
        try:
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            analysis_text = response.content[0].text
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            return {"error": f"AI analysis failed: {str(e)}"}
    
    def _build_analysis_prompt(self, report: Dict[str, Any]) -> str:
        return f"""
As a professional trading analyst, analyze the following comprehensive market data and provide trading insights:

MARKET DATA:
{json.dumps(report.get('market_data', {}), indent=2)}

NEWS SENTIMENT:
{json.dumps(report.get('news_sentiment', {}), indent=2)}

SOCIAL MEDIA SENTIMENT:
{json.dumps(report.get('social_sentiment', {}), indent=2)}

TECHNICAL ANALYSIS:
Charts available for: {list(report.get('technical_analysis', {}).keys())}

Please provide:
1. Overall market sentiment (Bullish/Bearish/Neutral)
2. Top 3 trading opportunities with reasoning
3. Risk assessment for each opportunity
4. Recommended position sizes (Conservative/Moderate/Aggressive)
5. Key levels to watch (support/resistance)
6. News catalysts that could impact prices

Format your response as structured JSON with the following keys:
- overall_sentiment
- trading_opportunities
- risk_assessment
- position_recommendations
- key_levels
- news_catalysts
- confidence_score (0-100)
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        try:
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text
            
            return json.loads(json_text)
        except json.JSONDecodeError:
            return {
                "overall_sentiment": "Unable to parse",
                "trading_opportunities": [],
                "risk_assessment": "Analysis parsing failed",
                "raw_response": response_text
            }
    
    async def generate_trade_alerts(self, analysis: Dict[str, Any], threshold: float = 0.7) -> List[Dict[str, Any]]:
        alerts = []

        confidence = analysis.get("confidence_score", 0) / 100
        if confidence < threshold:
            return alerts

        opportunities = analysis.get("trading_opportunities", [])
        timestamp = datetime.now().isoformat()
        for opportunity in opportunities:
            if isinstance(opportunity, dict):
                alert = {
                    "type": "trade_opportunity",
                    "symbol": opportunity.get("symbol", "Unknown"),
                    "action": opportunity.get("action", "Unknown"),
                    "reasoning": opportunity.get("reasoning", ""),
                    "confidence": confidence,
                    "timestamp": timestamp
                }
                alerts.append(alert)

        return alerts
    
    async def analyze_chart_with_vision(self, chart_path: str, symbol: str) -> Dict[str, Any]:
        if not chart_path or "error" in chart_path.lower():
            return {"error": "No chart available for analysis"}
        
        prompt = f"""
Analyze this TradingView chart for {symbol}. Identify:
1. Current trend direction
2. Key support and resistance levels
3. Technical indicators signals
4. Chart patterns
5. Potential entry/exit points
6. Risk/reward assessment

Provide a concise technical analysis with specific price levels.
"""
        
        try:
            with open(chart_path, "rb") as image_file:
                response = await self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_file.read()
                                }
                            }
                        ]
                    }]
                )
            
            return {"technical_analysis": response.content[0].text}
            
        except Exception as e:
            return {"error": f"Chart analysis failed: {str(e)}"}