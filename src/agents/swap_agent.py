"""Swap Agent — Token swap aggregation across DEXes."""
import json
import logging

logger = logging.getLogger("swap_agent")


class SwapAgent:
    """Finds best swap rates across multiple DEXes using MiMo AI."""

    def __init__(self, mimo_client, config: dict):
        self.mimo = mimo_client
        self.config = config
        self.dexes = config.get("dexes", ["uniswap", "sushiswap", "pancakeswap"])

    async def process(self, data: dict) -> dict:
        """Process a swap request and find best rate."""
        token_in = data.get("token_in", "ETH")
        token_out = data.get("token_out", "USDC")
        amount = data.get("amount", 1.0)

        # Get simulated rates from multiple DEXes
        rates = await self._fetch_rates(token_in, token_out, amount)

        # Use MiMo to analyze and recommend best route
        analysis = await self._analyze_rates(token_in, token_out, amount, rates)

        return {
            "token_in": token_in,
            "token_out": token_out,
            "amount": amount,
            "rates": rates,
            "recommendation": analysis,
            "best_dex": max(rates, key=lambda x: x["output_amount"])["dex"],
        }

    async def _fetch_rates(self, token_in: str, token_out: str, amount: float) -> list:
        """Fetch rates from all configured DEXes."""
        import random
        base_rate = 1850.0 if token_in == "ETH" and token_out == "USDC" else 1.0
        rates = []
        for dex in self.dexes:
            variation = random.uniform(0.98, 1.02)
            output = amount * base_rate * variation
            impact = random.uniform(0.001, 0.03)
            rates.append({
                "dex": dex,
                "output_amount": round(output, 2),
                "price_impact": round(impact * 100, 3),
                "gas_estimate": random.randint(100000, 300000),
                "liquidity": round(random.uniform(1000000, 50000000), 0),
            })
        return rates

    async def _analyze_rates(self, token_in, token_out, amount, rates) -> str:
        """Use MiMo to analyze and recommend best swap route."""
        messages = [
            {"role": "system", "content": "You are a DeFi swap optimization expert. Analyze the following DEX rates and recommend the best route considering price impact, gas costs, and liquidity. Be concise."},
            {"role": "user", "content": f"Swap {amount} {token_in} to {token_out}. Rates: {json.dumps(rates, indent=2)}"},
        ]
        try:
            result = await self.mimo.chat(messages=messages, agent_name="swap")
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"MiMo analysis failed: {e}")
            best = max(rates, key=lambda x: x["output_amount"])
            return f"Best rate: {best['dex']} with {best['output_amount']} {token_out}"
