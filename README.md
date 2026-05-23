# 🛡️ MiMoGuard

**DeFi Multi-Agent Intelligence Platform powered by Xiaomi MiMo AI**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![MiMo](https://img.shields.io/badge/Powered%20by-Xiaomi%20MiMo-orange.svg)](https://platform.xiaomimimo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🇨🇳 基于小米 MiMo 大模型的 DeFi 多智能体安全平台
>
> 4 specialized AI agents working 24/7 to protect your DeFi operations.

## 🏗️ Architecture

```
                        ┌──────────────────────┐
                        │    🧠 Orchestrator    │
                        │   MiMo-V2.5-Pro      │
                        └──────────┬───────────┘
                                   │
            ┌──────────┬───────────┼───────────┬──────────┐
       ┌────▼────┐ ┌───▼────┐ ┌───▼────┐ ┌───▼────┐     │
       │  🔍     │ │  🛡️   │ │  🔬    │ │  💡    │     │
       │  Swap   │ │ Threat │ │Auditor │ │Advisor │     │
       └─────────┘ └────────┘ └────────┘ └────────┘     │
       ┌─────────────────────────────────────────────────┘
       │              FastAPI REST API
       └──────────────────────┬──────────────
                        ┌─────▼─────┐
                        │ Next.js   │
                        │ Dashboard │
                        └───────────┘
```

## 🤖 Agent Fleet

- 🧠 **Orchestrator** — Central coordinator, event routing
- 🔍 **Swap Agent** — Token swap aggregation across DEXes
- 🛡️ **Threat Agent** — Real-time scam/rug pull detection
- 🔬 **Auditor** — 4-pass smart contract security analysis
- 💡 **Advisor** — AI-powered investment insights

## ⚡ Quick Start

```bash
git clone https://github.com/tonnkid/mimo-guard.git
cd mimo-guard
cp .env.example .env
pip install -r requirements.txt
python -m src.main

# Frontend
cd web && npm install && npm run dev
```

## 📡 API Endpoints

- `GET /health` — Health check
- `POST /api/swap/quote` — Get best swap rate
- `POST /api/audit/contract` — Audit smart contract
- `GET /api/threats` — Recent threats
- `GET /api/agents/status` — Agent status

## 🛠️ Tech Stack

- **AI**: Xiaomi MiMo V2.5 Pro
- **Backend**: Python 3.11 + FastAPI
- **Frontend**: Next.js 14 + Tailwind CSS
- **Blockchain**: Web3.py

## 📄 License

MIT — Built for 100T Xiaomi MiMo Competition
