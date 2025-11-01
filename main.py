# GrockPay Scanner - Detector de Memecoin Launches en Pump.fun
# Creado por @z3r0dev | Monetizado via PayPal: paypal.me/javieesolana
# Detecta carteras que lanzan tokens: patrones de tx a Pump program, mints rápidos.
# Adaptable: Busca por signatures recientes, no keys fijas.

import requests
from solders.pubkey import Pubkey  # pip install solders (solo para dev)
from datetime import datetime, timedelta

# Config: RPC gratuita de Solana (no necesitas SOL)
RPC_URL = "https://api.mainnet-beta.solana.com"
PUMP_PROGRAM_ID = Pubkey.from_string("6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P")  # Pump.fun program ID (fijo, no cambia)

def get_recent_signatures(limit=10):
    """Obtiene signatures recientes del programa Pump."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [str(PUMP_PROGRAM_ID), {"limit": limit}]
    }
    response = requests.post(RPC_URL, json=payload)
    return response.json().get('result', [])

def analyze_signature(sig):
    """Analiza tx: busca patrones de launch (e.g., mint + transfer SOL bajo)."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [sig['signature'], {"encoding": "json", "maxSupportedTransactionVersion": 0}]
    }
    response = requests.post(RPC_URL, json=payload)
    tx = response.json().get('result')
    if not tx:
        return None
    
    # Patrón: Busca instrucciones de mint/token create + fee bajo (indicador de launch)
    instructions = tx['transaction']['message']['instructions']
    is_launch = any('create' in str(inst.get('parsed', {}).get('type', '')) or 'mint' in str(inst) for inst in instructions)
    if is_launch:
        # Extrae wallet (feePayer)
        wallet = tx['transaction']['message']['accountKeys'][0]  # Primera key suele ser el launcher
        timestamp = datetime.fromtimestamp(sig['blockTime'])
        if (datetime.now() - timestamp) < timedelta(hours=1):  # Reciente
            return {
                'wallet': wallet,
                'signature': sig['signature'],
                'time': timestamp,
                'pattern': 'Posible memecoin launch detectado'
            }
    return None

def scan_launches():
    """Scan principal: Detecta y lista carteras suspicious."""
    sigs = get_recent_signatures(50)  # Más para precisión
    launches = []
    for sig in sigs:
        launch = analyze_signature(sig)
        if launch:
            launches.append(launch)
    return launches

# Run: python main.py
if __name__ == "__main__":
    print("🔍 GrockPay Scanner iniciado...")
    results = scan_launches()
    for r in results:
        print(f"🚨 {r['pattern']}: Wallet {r['wallet']} | Tx: https://solscan.io/tx/{r['signature']} | {r['time']}")
    if not results:
        print("No launches recientes. Observa patrones más tiempo.")
