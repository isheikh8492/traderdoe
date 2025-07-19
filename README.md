# Trading Copilot

AI-powered trading analysis tool that aggregates data from multiple sources using MCP (Model Context Protocol) servers and provides intelligent trading insights.

## Features

- **Multi-source Data Aggregation**: Yahoo Finance, Twitter/X, TradingView charts
- **AI-Powered Analysis**: Claude Sonnet 4 for comprehensive market analysis
- **Real-time Sentiment Analysis**: Social media and news sentiment tracking
- **Technical Analysis**: Chart pattern recognition via TradingView screenshots
- **Trade Alerts**: Automated opportunity detection with confidence scoring
- **Continuous Monitoring**: Real-time market surveillance

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and MCP server paths
   ```

3. **Install Required MCP Servers**
   
   **Yahoo Finance MCP:**
   ```bash
   git clone https://github.com/Alex2Yang97/yahoo-finance-mcp
   cd yahoo-finance-mcp
   pip install -e .
   ```
   
   **Twitter MCP:**
   ```bash
   # Check PulseMCP or GitHub for Twitter MCP server implementations
   ```
   
  **TradingView MCP:**
  ```bash
  git clone https://github.com/ertugrul59/tradingview-chart-mcp
  cd tradingview-chart-mcp
  pip install -e .
  ```

4. **Update Config**
   Edit `config.py` to match your MCP server installation paths.

## Usage

```bash
python main.py
```

**Options:**
1. **Single Analysis** - Run one-time market analysis
2. **Continuous Monitoring** - Monitor markets at set intervals
3. **Custom Symbols** - Analyze specific stock symbols

## Architecture

```
Trading Copilot
├── MCP Client Layer (mcp_client.py)
├── Data Aggregation (data_aggregator.py)
├── Sentiment Analysis (sentiment_analyzer.py)
├── AI Analysis (ai_analyzer.py)
└── Main Application (main.py)
```

## Required MCP Servers

- **Yahoo Finance MCP**: Stock data, financial news, market updates
- **Twitter/X MCP**: Social sentiment analysis
- **TradingView MCP**: Chart screenshots and technical analysis

## AI Models

**Primary**: Claude Sonnet 4
- Complex financial analysis
- Multi-modal chart interpretation
- 200K token context for comprehensive reports

## Configuration

Update `config.py` with:
- Trading symbols to monitor
- Sentiment analysis keywords
- API configurations

### MCP Server Configuration

MCP servers are defined in `mcp_servers/servers.yaml`. Each server entry
specifies the command used to launch it, command-line arguments, and an optional
`.env` file containing server‑specific variables. Example:

```yaml
servers:
  tradingview:
    command: python
    args:
      - ${TRADINGVIEW_CHART_MCP_PATH}/server.py
    env_file: tradingview_chart/.env
```

Environment files live inside the `mcp_servers/<server>/` directories. Copy the
provided `.env.example` for each server and adjust the values to your setup.

## Example Output

```
📈 TRADING COPILOT ANALYSIS REPORT
============================================================

🎯 Overall Sentiment: Bullish
🎲 Confidence Score: 85%

💡 Trading Opportunities:
  1. AAPL - BUY
     Reason: Strong earnings beat + positive social sentiment
  2. TSLA - HOLD
     Reason: Mixed signals, await breakout confirmation

🚨 Active Alerts: 2
  • AAPL: BUY signal detected
  • NVDA: High volume spike

⏰ Generated at: 2025-07-18T10:30:00
============================================================
```

## Security

- All API keys stored in environment variables
- No sensitive data logged or committed
- MCP servers run in isolated processes
