"""Multi-chain Web3 provider manager."""
import logging
from typing import Optional

logger = logging.getLogger("blockchain")


class BlockchainManager:
    """Manages Web3 connections to multiple chains."""

    SUPPORTED_CHAINS = {
        "ethereum": {"chain_id": 1, "name": "Ethereum"},
        "base": {"chain_id": 8453, "name": "Base"},
        "arbitrum": {"chain_id": 42161, "name": "Arbitrum"},
    }

    def __init__(self, config: dict):
        self.config = config
        self.providers = {}

    def get_chain_info(self, chain: str) -> Optional[dict]:
        return self.SUPPORTED_CHAINS.get(chain)

    def get_supported_chains(self) -> list[str]:
        return list(self.SUPPORTED_CHAINS.keys())
