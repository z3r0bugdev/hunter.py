from solders.pubkey import Pubkey
from solders.signature import Signature
import requests

def is_valid_pubkey(key_str: str) -> bool:
    """Valida si es una Pubkey válida de Solana."""
    try:
        Pubkey.from_string(key_str)
        return True
    except ValueError:
        return False

def fetch_token_metadata(mint: str) -> dict:
    """Obtiene metadata de token via API externa (e.g., Solana FM)."""
    try:
        url = f"https://api.solanafm.com/token/{mint}"
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else {}
    except requests.RequestException:
        return {}

def check_liquidity(mint: str, rpc_url: str) -> float:
    """Verifica liquidez básica (simplificado: chequea pool size). En prod, usa Raydium SDK."""
    # Placeholder: En real, query accounts por mint y suma SOL en pools
    return 0.0  # Retorna en SOL; implementa con get_token_accounts_by_owner