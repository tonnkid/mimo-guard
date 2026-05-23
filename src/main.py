#!/usr/bin/env python3
"""MiMoGuard — Main Entry Point

DeFi Multi-Agent Intelligence Platform powered by Xiaomi MiMo AI.
"""
import argparse
import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-12s | %(levelname)-5s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mimoguard")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="MiMoGuard — DeFi Multi-Agent Platform")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    logger.info("🛡️ MiMoGuard starting...")
    logger.info(f"   API:   http://{args.host}:{args.port}")
    logger.info(f"   Docs:  http://{args.host}:{args.port}/docs")
    logger.info(f"   Model: Xiaomi MiMo V2.5 Pro")

    uvicorn.run(
        "src.api.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
