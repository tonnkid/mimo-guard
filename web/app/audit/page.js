"use client";

import { useState } from "react";

export default function AuditPage() {
  const [address, setAddress] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pass, setPass] = useState(0);

  const analyze = async () => {
    if (!address) return;
    setLoading(true);
    setResult(null);
    setPass(0);

    // Simulate 4-pass analysis
    const passes = [
      { name: "Bytecode Analysis", icon: "🔍" },
      { name: "Function Selector Mapping", icon: "📋" },
      { name: "Vulnerability Scanning", icon: "🛡️" },
      { name: "Deep Reasoning (MiMo-V2.5-Pro)", icon: "🧠" },
    ];

    for (let i = 0; i < passes.length; i++) {
      await new Promise(r => setTimeout(r, 1000));
      setPass(i + 1);
    }

    setResult({
      riskScore: 23,
      verdict: "safe",
      findings: [
        { severity: "info", msg: "Standard ERC-20 token implementation detected" },
        { severity: "info", msg: "No proxy patterns found" },
        { severity: "low", msg: "Minor: No event emission on transfer" },
        { severity: "info", msg: "No selfdestruct opcode found" },
        { severity: "info", msg: "No external calls to untrusted contracts" },
      ],
      recommendation: "Contract appears safe for interaction. Standard ERC-20 implementation with no critical vulnerabilities detected.",
    });
    setLoading(false);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">🔬 Smart Contract Auditor</h1>
        <p className="text-zinc-500">4-pass deep analysis powered by MiMo-V2.5-Pro</p>
      </div>

      <div className="glass rounded-xl p-8 space-y-4">
        <label className="text-sm text-zinc-500 block">Contract Address</label>
        <div className="flex gap-3">
          <input value={address} onChange={e => setAddress(e.target.value)}
            className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-3 font-mono focus:border-orange-500 outline-none"
            placeholder="0x..." />
          <button onClick={analyze} disabled={loading}
            className="px-6 py-3 bg-orange-500 hover:bg-orange-600 rounded-lg font-bold transition disabled:opacity-50">
            {loading ? "⏳" : "🔬"} Analyze
          </button>
        </div>
      </div>

      {/* Pass Progress */}
      {loading && (
        <div className="glass rounded-xl p-6 space-y-3">
          <h3 className="font-bold">Analysis Progress</h3>
          {["Bytecode Analysis", "Function Selector Mapping", "Vulnerability Scanning", "Deep Reasoning"].map((name, i) => (
            <div key={name} className="flex items-center gap-3">
              <span className={i < pass ? "text-green-500" : i === pass ? "text-orange-500 animate-pulse" : "text-zinc-600"}>
                {i < pass ? "✅" : i === pass ? "⏳" : "⏸️"}
              </span>
              <span className={i < pass ? "text-zinc-300" : i === pass ? "text-orange-400" : "text-zinc-600"}>
                Pass {i + 1}: {name}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-4">
          <div className="glass rounded-xl p-8 text-center">
            <div className="text-6xl mb-4">{result.verdict === "safe" ? "✅" : "⚠️"}</div>
            <div className={`text-5xl font-bold ${result.riskScore < 30 ? "text-green-500" : result.riskScore < 60 ? "text-amber-500" : "text-red-500"}`}>
              {result.riskScore}/100
            </div>
            <div className="text-zinc-500 mt-2">Risk Score</div>
            <div className={`mt-2 inline-block px-4 py-1 rounded-full text-sm font-bold ${
              result.verdict === "safe" ? "bg-green-500/10 text-green-500" : "bg-red-500/10 text-red-500"
            }`}>
              {result.verdict.toUpperCase()}
            </div>
          </div>

          <div className="glass rounded-xl p-6">
            <h3 className="font-bold mb-3">Findings</h3>
            <div className="space-y-2">
              {result.findings.map((f, i) => (
                <div key={i} className="flex gap-3 text-sm">
                  <span className={f.severity === "high" ? "text-red-500" : f.severity === "medium" ? "text-amber-500" : f.severity === "low" ? "text-yellow-500" : "text-green-500"}>
                    {f.severity === "info" ? "✅" : f.severity === "low" ? "⚠️" : "🚨"}
                  </span>
                  <span className="text-zinc-300">{f.msg}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="glass rounded-xl p-6">
            <h3 className="font-bold mb-2">🤖 MiMo Recommendation</h3>
            <p className="text-zinc-400">{result.recommendation}</p>
          </div>
        </div>
      )}
    </div>
  );
}
