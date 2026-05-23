"""Price Feed — Token price service."""
import logging

logger = logging.getLogger("price_feed")


class PriceFeed:
    """Provides token price data."""

    MOCK_PRICES = {
        "ETH": 1850.00, "BTC": 67000.00, "USDC": 1.00,
        "USDT": 1.00, "DAI": 1.00, "LINK": 14.50,
        "UNI": 7.20, "AAVE": 95.00, "ARB": 1.15,
    }

    def get_price(self, token: str) -> float:
        return self.MOCK_PRICES.get(token.upper(), 0.0)

    def get_prices(self, tokens: list[str]) -> dict:
        return {t: self.get_price(t) for t in tokens}
