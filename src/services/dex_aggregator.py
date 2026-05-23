"""DEX Aggregator — Simulated rate comparison across DEXes."""
import random
import logging

logger = logging.getLogger("dex_aggregator")


class DexAggregator:
    """Compares token swap rates across multiple DEXes."""

    DEXES = {
        "uniswap": {"fee": 0.003, "name": "Uniswap V3"},
        "sushiswap": {"fee": 0.003, "name": "SushiSwap"},
        "pancakeswap": {"fee": 0.0025, "name": "PancakeSwap"},
    }

    PRICE_BASES = {
        ("ETH", "USDC"): 1850.0,
        ("ETH", "USDT"): 1850.0,
        ("BTC", "USDC"): 67000.0,
        ("USDC", "USDT"): 1.0,
        ("DAI", "USDC"): 1.0,
    }

    def get_rates(self, token_in: str, token_out: str, amount: float) -> list:
        """Get simulated rates from all DEXes."""
        base_price = self.PRICE_BASES.get((token_in, token_out), 1.0)
        rates = []

        for dex_id, dex_info in self.DEXES.items():
            variation = random.uniform(0.985, 1.015)
            output = amount * base_price * (1 - dex_info["fee"]) * variation
            impact = random.uniform(0.001, 0.05) * (amount / 10)
            gas = random.randint(100000, 300000)

            rates.append({
                "dex": dex_id,
                "dex_name": dex_info["name"],
                "output_amount": round(output, 6),
                "fee": dex_info["fee"],
                "price_impact": round(min(impact, 0.15) * 100, 3),
                "gas_estimate": gas,
                "gas_cost_usd": round(gas * 0.00000002 * 1850, 2),
                "liquidity": round(random.uniform(5000000, 100000000), 0),
            })

        return sorted(rates, key=lambda x: x["output_amount"], reverse=True)
