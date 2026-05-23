"""Threat Agent — Real-time scam/rug pull detection."""
import logging
import random
from datetime import datetime

logger = logging.getLogger("threat_agent")


class ThreatAgent:
    """Real-time DeFi threat detection and monitoring."""

    THREAT_TYPES = [
        "rug_pull", "honeypot", "flash_loan_attack",
        "phishing", "fake_token", "oracle_manipulation"
    ]

    def __init__(self, mimo_client, config: dict):
        self.mimo = mimo_client
        self.config = config
        self.alert_threshold = config.get("alert_threshold", 0.80)
        self.recent_threats = []

    async def scan(self, data: dict) -> dict:
        """Scan for threats in transaction or contract data."""
        target = data.get("target", "")
        scan_type = data.get("type", "transaction")

        messages = [
            {"role": "system", "content": "You are a DeFi security analyst. Analyze the following data for potential threats (rug pull, honeypot, flash loan attack, phishing). Return JSON with: threat_type, risk_level (low/medium/high/critical), confidence (0-1), explanation."},
            {"role": "user", "content": f"Scan type: {scan_type}\nTarget: {target}\nData: {str(data)}"},
        ]

        try:
            result = await self.mimo.chat(messages=messages, agent_name="threat")
            analysis = result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"MiMo analysis failed: {e}")
            analysis = "Analysis unavailable"

        threat = {
            "target": target,
            "scan_type": scan_type,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "analyzed",
        }
        self.recent_threats.append(threat)
        if len(self.recent_threats) > 100:
            self.recent_threats = self.recent_threats[-100:]

        return threat

    async def get_recent_threats(self, limit: int = 20) -> list:
        return self.recent_threats[-limit:]
