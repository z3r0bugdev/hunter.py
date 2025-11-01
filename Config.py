import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
    ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")
    MIN_LIQUIDITY = int(os.getenv("MIN_LIQUIDITY", "1000000000"))
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "1"))
    PUMP_FUN_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"  # Pump.fun program ID

config = Config()