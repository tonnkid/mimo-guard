"""Orchestrator Agent — Central coordination hub for all agents."""
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger("orchestrator")


class OrchestratorAgent:
    """Central event-driven coordinator managing all specialized agents."""

    def __init__(self, mimo_client, config: dict):
        self.mimo = mimo_client
        self.config = config
        self.agents = {}
        self.event_queue = asyncio.Queue(maxsize=10000)
        self.stats = {
            "events_processed": 0,
            "threats_detected": 0,
            "contracts_audited": 0,
            "swaps_analyzed": 0,
            "start_time": datetime.utcnow().isoformat(),
        }

    def register_agent(self, name: str, agent):
        self.agents[name] = agent
        logger.info(f"Agent registered: {name}")

    async def dispatch(self, event: dict):
        """Route events to appropriate agents."""
        event_type = event.get("type", "")
        self.stats["events_processed"] += 1

        if event_type == "swap_request":
            if "swap" in self.agents:
                return await self.agents["swap"].process(event["data"])
        elif event_type == "audit_request":
            if "auditor" in self.agents:
                self.stats["contracts_audited"] += 1
                return await self.agents["auditor"].analyze(event["data"])
        elif event_type == "threat_scan":
            if "threat" in self.agents:
                self.stats["threats_detected"] += 1
                return await self.agents["threat"].scan(event["data"])
        elif event_type == "advice_request":
            if "advisor" in self.agents:
                return await self.agents["advisor"].advise(event["data"])

        return {"error": f"Unknown event type: {event_type}"}

    def get_status(self) -> dict:
        return {
            "agents": {name: "online" for name in self.agents},
            "stats": self.stats,
            "mimo_usage": self.mimo.get_usage(),
        }
