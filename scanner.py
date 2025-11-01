import asyncio
import logging
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey
from config import config
from alerts import send_alert

logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self):
        self.client = AsyncClient(config.SOLANA_RPC_URL)
        self.pump_program = Pubkey.from_string(config.PUMP_FUN_PROGRAM_ID)
        self.processed_signatures = set()  # Evita duplicados

    async def scan_for_launches(self):
        """Escanea logs para nuevas creaciones de tokens en Pump.fun."""
        try:
            # Usa get_signatures_for_address para polling eficiente
            signatures = await self.client.get_signatures_for_address(
                self.pump_program, limit=10, commitment=Confirmed
            )
            for sig_info in signatures.value:
                sig = str(sig_info.signature)
                if sig in self.processed_signatures:
                    continue
                self.processed_signatures.add(sig)

                # Fetch tx details
                tx = await self.client.get_transaction(sig, encoding="json", commitment=Confirmed)
                if not tx.value:
                    continue

                # Parse para 'create' instruction (nuevo memecoin)
                if self._is_new_memecoin(tx.value.transaction):
                    mint = self._extract_mint(tx.value.transaction)
                    if not mint:
                        continue

                    # Chequea rotación de wallet (simplificado: chequea si creator en lista conocida)
                    creator = self._extract_creator(tx.value.transaction)
                    is_rotating = await self._check_wallet_rotation(creator)

                    liquidity = await self._check_liquidity(mint)  # En utils
                    metadata = fetch_token_metadata(mint)  # En utils

                    alert_data = {
                        "mint": mint,
                        "signature": sig,
                        "creator": creator,
                        "is_rotating": is_rotating,
                        "liquidity": liquidity,
                        "metadata": metadata,
                        "rug_risk": liquidity < config.MIN_LIQUIDITY
                    }
                    await send_alert(alert_data)

            await asyncio.sleep(config.POLL_INTERVAL)
        except Exception as e:
            logger.error(f"Error en scan: {e}")
            await asyncio.sleep(5)  # Backoff

    def _is_new_memecoin(self, tx) -> bool:
        # Chequea si la instrucción es 'create' en Pump.fun
        # Implementa parsing de instructions (usa tx.message.instructions)
        return True  # Placeholder; parse real con solders

    def _extract_mint(self, tx) -> str | None:
        # Extrae mint address de la tx
        return "ExampleMint11111111111111111111111111111111"  # Placeholder

    def _extract_creator(self, tx) -> str:
        # Extrae signer/creator
        return "ExampleCreatorPubkey"  # Placeholder

    async def _check_wallet_rotation(self, creator: str) -> bool:
        # Chequea si creator ha cambiado recientemente (query tx history)
        return False  # Placeholder; usa get_signatures_for_address en creator

    async def _check_liquidity(self, mint: str) -> float:
        return check_liquidity(mint, config.SOLANA_RPC_URL)  # De utils

    async def run(self):
        logger.info("Iniciando escáner...")
        while True:
            await self.scan_for_launches()