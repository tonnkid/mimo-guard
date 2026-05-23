"""Auditor Agent — 4-pass smart contract security analysis."""
import logging

logger = logging.getLogger("auditor")


class AuditorAgent:
    """Performs deep smart contract security analysis using 4-pass MiMo reasoning."""

    def __init__(self, mimo_client, config: dict):
        self.mimo = mimo_client
        self.passes = config.get("passes", 4)
        self.min_confidence = config.get("min_confidence", 0.85)

    async def analyze(self, data: dict) -> dict:
        """Run 4-pass analysis on a smart contract."""
        contract_address = data.get("address", "")
        chain = data.get("chain", "ethereum")
        bytecode = data.get("bytecode", "0x")

        results = {}

        # Pass 1: Bytecode Analysis
        logger.info("[Pass 1/4] Bytecode analysis...")
        results["bytecode"] = await self._pass_bytecode(bytecode, contract_address)

        # Pass 2: Function Selector Mapping
        logger.info("[Pass 2/4] Function selector mapping...")
        results["selectors"] = await self._pass_selectors(bytecode)

        # Pass 3: Vulnerability Pattern Detection
        logger.info("[Pass 3/4] Vulnerability scanning...")
        results["vulnerabilities"] = await self._pass_vulnerabilities(bytecode, contract_address)

        # Pass 4: Deep Reasoning (MiMo-V2.5-Pro)
        logger.info("[Pass 4/4] Deep reasoning analysis...")
        results["assessment"] = await self._pass_deep_reasoning(contract_address, results)

        return {
            "contract": contract_address,
            "chain": chain,
            "passes": results,
            "risk_score": self._calculate_risk(results),
            "safe": self._calculate_risk(results) < 50,
        }

    async def _pass_bytecode(self, bytecode: str, address: str) -> dict:
        messages = [
            {"role": "system", "content": "Analyze EVM bytecode. Identify contract type, proxy patterns, and storage layout. Return JSON with: contract_type, is_proxy, complexity_score."},
            {"role": "user", "content": f"Address: {address}\nBytecode (first 500 chars): {bytecode[:500]}"},
        ]
        try:
            result = await self.mimo.chat(messages=messages, agent_name="auditor-p1")
            return {"analysis": result["choices"][0]["message"]["content"], "status": "complete"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    async def _pass_selectors(self, bytecode: str) -> dict:
        messages = [
            {"role": "system", "content": "Map function selectors from EVM bytecode. Identify known dangerous functions (selfdestruct, delegatecall). Return JSON."},
            {"role": "user", "content": f"Bytecode: {bytecode[:500]}"},
        ]
        try:
            result = await self.mimo.chat(messages=messages, agent_name="auditor-p2")
            return {"analysis": result["choices"][0]["message"]["content"], "status": "complete"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    async def _pass_vulnerabilities(self, bytecode: str, address: str) -> dict:
        messages = [
            {"role": "system", "content": "Detect vulnerability patterns: reentrancy, integer overflow, unchecked calls, front-running risks. Return JSON with severity levels."},
            {"role": "user", "content": f"Contract: {address}\nBytecode: {bytecode[:500]}"},
        ]
        try:
            result = await self.mimo.chat(messages=messages, agent_name="auditor-p3")
            return {"analysis": result["choices"][0]["message"]["content"], "status": "complete"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    async def _pass_deep_reasoning(self, address: str, prev_results: dict) -> dict:
        messages = [
            {"role": "system", "content": "You are a senior smart contract auditor. Synthesize the following analysis passes into a final security assessment. Return JSON with: risk_score (0-100), verdict (safe/warning/danger), findings, recommendation."},
            {"role": "user", "content": f"Contract: {address}\nPrevious analysis: {str(prev_results)[:2000]}"},
        ]
        try:
            result = await self.mimo.chat(messages=messages, agent_name="auditor-p4", model=self.mimo.model_primary)
            return {"analysis": result["choices"][0]["message"]["content"], "status": "complete"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def _calculate_risk(self, results: dict) -> int:
        """Calculate overall risk score from all passes."""
        failed = sum(1 for v in results.values() if isinstance(v, dict) and v.get("status") == "failed")
        if failed >= 3:
            return 90
        elif failed >= 2:
            return 70
        elif failed >= 1:
            return 50
        return 25
