"""Advisor Agent — AI-powered investment insights."""
import logging

logger = logging.getLogger("advisor")


class AdvisorAgent:
    """Provides AI-powered DeFi investment advice using MiMo."""

    def __init__(self, mimo_client, config: dict):
        self.mimo = mimo_client

    async def advise(self, data: dict) -> dict:
        """Provide investment advice based on user query."""
        query = data.get("query", "")
        portfolio = data.get("portfolio", {})

        messages = [
            {"role": "system", "content": "You are a DeFi investment advisor. Provide clear, actionable advice. Always include risk warnings. Be concise and practical."},
            {"role": "user", "content": f"Query: {query}\nPortfolio: {portfolio}"},
        ]

        try:
            result = await self.mimo.chat(messages=messages, agent_name="advisor")
            advice = result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"MiMo analysis failed: {e}")
            advice = "Unable to generate advice at this time."

        return {
            "query": query,
            "advice": advice,
            "disclaimer": "This is AI-generated advice, not financial advice. Always DYOR.",
        }
