import logging
import requests
import json
from config import config

logger = logging.getLogger(__name__)

async def send_alert(data: dict):
    """Envía alerta a consola y webhook si configurado."""
    message = f"🆕 Nuevo Memecoin Detectado!\nMint: {data['mint']}\nSig: {data['signature']}\nCreator: {data['creator']}\nRug Risk: {data['rug_risk']}\nLiquidez: {data['liquidity']} SOL"
    
    print(message)  # Consola básica
    
    if config.ALERT_WEBHOOK_URL:
        try:
            payload = {"content": message}
            requests.post(config.ALERT_WEBHOOK_URL, json=payload, timeout=5)
            logger.info("Alerta enviada via webhook")
        except requests.RequestException as e:
            logger.error(f"Error en webhook: {e}")
    
    # Opcional: Export a CSV
    # with open('launches.csv', 'a') as f: ... 