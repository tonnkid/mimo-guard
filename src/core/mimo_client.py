"""MiMo API Client — OpenAI-compatible wrapper with dual-key round-robin."""
import asyncio
import time
import logging
from dataclasses import dataclass, field
from typing import Optional

import httpx

logger = logging.getLogger("mimo_client")


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    requests: int = 0


class MiMoClient:
    """Xiaomi MiMo API client with dual-key round-robin and rate limiting."""

    def __init__(
        self,
        api_url: str,
        api_keys: list[str],
        model_primary: str = "mimo-v2.5-pro",
        model_secondary: str = "mimo-v2.5",
        max_tokens: int = 32000,
        requests_per_minute: int = 60,
    ):
        self.api_url = api_url.rstrip("/")
        self.api_keys = api_keys
        self._key_index = 0
        self.model_primary = model_primary
        self.model_secondary = model_secondary
        self.max_tokens = max_tokens
        self.rpm_limit = requests_per_minute
        self._client = httpx.AsyncClient(timeout=120)
        self._usage = TokenUsage()
        self._request_times: list[float] = []

    def _next_key(self) -> str:
        """Round-robin between API keys."""
        key = self.api_keys[self._key_index % len(self.api_keys)]
        self._key_index += 1
        return key

    async def _rate_limit(self):
        """Enforce rate limiting per key."""
        now = time.monotonic()
        self._request_times = [t for t in self._request_times if now - t < 60]
        if len(self._request_times) >= self.rpm_limit:
            wait = 60 - (now - self._request_times[0])
            if wait > 0:
                logger.warning(f"Rate limit hit, waiting {wait:.1f}s")
                await asyncio.sleep(wait)
        self._request_times.append(time.monotonic())

    async def chat(
        self,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        agent_name: str = "unknown",
    ) -> dict:
        """Send chat completion request to MiMo API with retry."""
        model = model or self.model_primary
        await self._rate_limit()

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens or self.max_tokens,
        }

        for attempt in range(3):
            try:
                key = self._next_key()
                start = time.monotonic()
                resp = await self._client.post(
                    f"{self.api_url}/chat/completions",
                    json=payload,
                    headers={"Authorization": f"Bearer {key}"},
                )
                elapsed = time.monotonic() - start
                resp.raise_for_status()
                data = resp.json()

                # Track usage
                usage = data.get("usage", {})
                self._usage.prompt_tokens += usage.get("prompt_tokens", 0)
                self._usage.completion_tokens += usage.get("completion_tokens", 0)
                self._usage.total_tokens += usage.get("total_tokens", 0)
                self._usage.requests += 1

                logger.info(
                    f"[{agent_name}] {model} | "
                    f"tokens={usage.get('total_tokens', 0)} | "
                    f"time={elapsed:.2f}s"
                )
                return data

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < 2:
                    wait = 2 ** (attempt + 1)
                    logger.warning(f"429 rate limited, retry in {wait}s")
                    await asyncio.sleep(wait)
                    continue
                raise
            except Exception as e:
                if attempt < 2:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise

    def get_usage(self) -> dict:
        return {
            "prompt_tokens": self._usage.prompt_tokens,
            "completion_tokens": self._usage.completion_tokens,
            "total_tokens": self._usage.total_tokens,
            "requests": self._usage.requests,
        }

    async def close(self):
        await self._client.aclose()
