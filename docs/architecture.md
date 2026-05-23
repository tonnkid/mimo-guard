# MiMoGuard Architecture

## Overview

MiMoGuard is a DeFi Multi-Agent Intelligence Platform powered by Xiaomi MiMo AI.

## Agent Communication Flow

```
User Request → FastAPI → Orchestrator → Specialized Agent → MiMo API → Response
```

## MiMo Integration

All agents use Xiaomi MiMo V2.5 Pro for:
- Natural language understanding
- Smart contract analysis
- Threat pattern recognition
- Investment advice generation

## Tech Stack

- Backend: Python 3.11 + FastAPI
- Frontend: Next.js 14 + Tailwind CSS
- AI: Xiaomi MiMo V2.5 Pro
- Blockchain: Web3.py
