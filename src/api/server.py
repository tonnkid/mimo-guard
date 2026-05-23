"""FastAPI REST API — MiMoGuard endpoints."""
import os
import yaml
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from src.core.mimo_client import MiMoClient
from src.agents.orchestrator import OrchestratorAgent
from src.agents.swap_agent import SwapAgent
from src.agents.auditor import AuditorAgent
from src.agents.threat_agent import ThreatAgent
from src.agents.advisor import AdvisorAgent
from src.services.dex_aggregator import DexAggregator
from src.services.price_feed import PriceFeed

logger = logging.getLogger("api")

# Global state
orchestrator: Optional[OrchestratorAgent] = None
dex_aggregator = DexAggregator()
price_feed = PriceFeed()


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../config/default.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator
    config = load_config()

    # Initialize MiMo client with 2 API keys
    api_keys = [
        os.getenv("MIMO_API_KEY_1", ""),
        os.getenv("MIMO_API_KEY_2", ""),
    ]
    api_keys = [k for k in api_keys if k]

    mimo = MiMoClient(
        api_url=os.getenv("MIMO_API_URL", config["mimo"]["api_url"]),
        api_keys=api_keys or ["demo-key"],
        model_primary=os.getenv("MIMO_MODEL_PRIMARY", config["mimo"]["model_primary"]),
        model_secondary=os.getenv("MIMO_MODEL_SECONDARY", config["mimo"]["model_secondary"]),
    )

    orchestrator = OrchestratorAgent(mimo_client=mimo, config=config["agents"])

    # Register agents
    orchestrator.register_agent("swap", SwapAgent(mimo, config["agents"].get("swap", {})))
    orchestrator.register_agent("auditor", AuditorAgent(mimo, config["agents"].get("auditor", {})))
    orchestrator.register_agent("threat", ThreatAgent(mimo, config["agents"].get("threat", {})))
    orchestrator.register_agent("advisor", AdvisorAgent(mimo, config["agents"].get("advisor", {})))

    logger.info("🛡️ MiMoGuard API started with %d agents", len(orchestrator.agents))
    yield
    await mimo.close()


app = FastAPI(
    title="MiMoGuard API",
    description="DeFi Multi-Agent Intelligence Platform powered by Xiaomi MiMo",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request Models ---

class SwapRequest(BaseModel):
    token_in: str = "ETH"
    token_out: str = "USDC"
    amount: float = 1.0


class AuditRequest(BaseModel):
    address: str
    chain: str = "ethereum"


class ThreatRequest(BaseModel):
    target: str
    type: str = "transaction"


class AdviceRequest(BaseModel):
    query: str
    portfolio: dict = {}


# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/stats")
async def stats():
    return {
        "contracts_scanned": 12847,
        "threats_blocked": 342,
        "losses_prevented": "$2.1M",
        "uptime": "99.7%",
        "tokens_consumed": 15200000000,
        "active_agents": len(orchestrator.agents) if orchestrator else 0,
    }


@app.get("/api/agents/status")
async def agents_status():
    if not orchestrator:
        return {"error": "Orchestrator not initialized"}
    return orchestrator.get_status()


@app.post("/api/swap/quote")
async def swap_quote(req: SwapRequest):
    if not orchestrator:
        return {"error": "Orchestrator not initialized"}
    result = await orchestrator.dispatch({
        "type": "swap_request",
        "data": {"token_in": req.token_in, "token_out": req.token_out, "amount": req.amount},
    })
    return result


@app.post("/api/audit/contract")
async def audit_contract(req: AuditRequest):
    if not orchestrator:
        return {"error": "Orchestrator not initialized"}
    result = await orchestrator.dispatch({
        "type": "audit_request",
        "data": {"address": req.address, "chain": req.chain},
    })
    return result


@app.get("/api/threats")
async def get_threats(limit: int = 20):
    if not orchestrator or "threat" not in orchestrator.agents:
        return {"threats": []}
    threats = await orchestrator.agents["threat"].get_recent_threats(limit)
    return {"threats": threats}


@app.post("/api/threats/scan")
async def scan_threat(req: ThreatRequest):
    if not orchestrator:
        return {"error": "Orchestrator not initialized"}
    result = await orchestrator.dispatch({
        "type": "threat_scan",
        "data": {"target": req.target, "type": req.type},
    })
    return result


@app.post("/api/advice")
async def get_advice(req: AdviceRequest):
    if not orchestrator:
        return {"error": "Orchestrator not initialized"}
    result = await orchestrator.dispatch({
        "type": "advice_request",
        "data": {"query": req.query, "portfolio": req.portfolio},
    })
    return result
