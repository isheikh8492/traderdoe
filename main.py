import asyncio
import json
from datetime import datetime
from config import Config
from mcp_client import MCPClient
from data_aggregator import DataAggregator
from ai_analyzer import AIAnalyzer

class TradingCopilot:
    def __init__(self):
        self.config = Config()
        self.mcp_client = MCPClient(self.config.MCP_SERVERS)
        self.data_aggregator = DataAggregator(self.mcp_client)
        self.ai_analyzer = AIAnalyzer(self.config.ANTHROPIC_API_KEY)
        
    async def initialize(self):
        print("🚀 Initializing Trading Copilot...")
        await self.mcp_client.connect_to_servers()
        print("✅ MCP servers connected")
        
    async def run_analysis(self, symbols: list = None):
        if symbols is None:
            symbols = self.config.TRADING_SYMBOLS
            
        print(f"📊 Analyzing symbols: {', '.join(symbols)}")
        
        comprehensive_report = await self.data_aggregator.generate_comprehensive_report(symbols)
        
        print("🤖 Running AI analysis...")
        ai_analysis = await self.ai_analyzer.analyze_trading_data(comprehensive_report)
        
        trade_alerts = await self.ai_analyzer.generate_trade_alerts(ai_analysis)
        
        final_report = {
            "comprehensive_data": comprehensive_report,
            "ai_analysis": ai_analysis,
            "trade_alerts": trade_alerts,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        self.display_results(final_report)
        return final_report
        
    def display_results(self, report: dict):
        print("\n" + "="*60)
        print("📈 TRADING COPILOT ANALYSIS REPORT")
        print("="*60)
        
        ai_analysis = report.get("ai_analysis", {})
        
        print(f"\n🎯 Overall Sentiment: {ai_analysis.get('overall_sentiment', 'Unknown')}")
        print(f"🎲 Confidence Score: {ai_analysis.get('confidence_score', 0)}%")
        
        opportunities = ai_analysis.get("trading_opportunities", [])
        if opportunities:
            print("\n💡 Trading Opportunities:")
            for i, opp in enumerate(opportunities[:3], 1):
                if isinstance(opp, dict):
                    print(f"  {i}. {opp.get('symbol', 'N/A')} - {opp.get('action', 'N/A')}")
                    print(f"     Reason: {opp.get('reasoning', 'N/A')}")
        
        alerts = report.get("trade_alerts", [])
        if alerts:
            print(f"\n🚨 Active Alerts: {len(alerts)}")
            for alert in alerts:
                print(f"  • {alert.get('symbol', 'N/A')}: {alert.get('action', 'N/A')}")
        
        print(f"\n⏰ Generated at: {report.get('analysis_timestamp', 'Unknown')}")
        print("="*60)
        
    async def run_continuous_monitoring(self, interval_minutes: int = 15):
        print(f"🔄 Starting continuous monitoring (every {interval_minutes} minutes)")
        
        while True:
            try:
                await self.run_analysis()
                await asyncio.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("\n⏹️ Stopping continuous monitoring...")
                break
            except Exception as e:
                print(f"❌ Error in monitoring: {e}")
                await asyncio.sleep(60)
                
    async def cleanup(self):
        await self.mcp_client.close_connections()
        print("🧹 Cleanup completed")

async def main():
    copilot = TradingCopilot()
    
    try:
        await copilot.initialize()
        
        print("\nTrading Copilot Options:")
        print("1. Run single analysis")
        print("2. Start continuous monitoring")
        print("3. Analyze specific symbols")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            await copilot.run_analysis()
        elif choice == "2":
            interval = int(input("Monitoring interval in minutes (default 15): ") or "15")
            await copilot.run_continuous_monitoring(interval)
        elif choice == "3":
            symbols_input = input("Enter symbols (comma-separated, e.g., AAPL,GOOGL): ")
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            await copilot.run_analysis(symbols)
        else:
            print("Invalid choice. Running single analysis...")
            await copilot.run_analysis()
            
    except Exception as e:
        print(f"❌ Application error: {e}")
    finally:
        await copilot.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
