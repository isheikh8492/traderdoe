import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent

# Load root .env first
load_dotenv()


def _load_mcp_servers() -> dict:
    """Load MCP server configurations from mcp_servers/servers.yaml."""
    config_file = ROOT_DIR / "mcp_servers" / "servers.yaml"
    if not config_file.exists():
        return {}
    with open(config_file, "r") as f:
        data = yaml.safe_load(f) or {}
    servers = {}
    for name, cfg in data.get("servers", {}).items():
        env_file = cfg.get("env_file")
        if env_file:
            env_path = ROOT_DIR / "mcp_servers" / env_file
            if env_path.exists():
                load_dotenv(env_path, override=False)
        command = os.path.expandvars(cfg.get("command", ""))
        args = [os.path.expandvars(a) for a in cfg.get("args", [])]
        servers[name] = {"command": command, "args": args}
    return servers


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MCP_SERVERS = _load_mcp_servers()

    TRADING_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "SPY", "QQQ"]

    SENTIMENT_KEYWORDS = [
        "bullish", "bearish", "buy", "sell", "pump", "dump",
        "moon", "crash", "breakout", "support", "resistance"
    ]
