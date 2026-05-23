"use client";

import { useState, useEffect } from "react";

const mockThreats = [
  { id: 1, type: "rug_pull", target: "0x7a25...f8c2", risk: "critical", chain: "Ethereum", time: "2 min ago", desc: "Contract drained liquidity pool — $142K stolen" },
  { id: 2, type: "honeypot", target: "0x3bc4...9d1a", risk: "high", chain: "Base", time: "5 min ago", desc: "Token contract prevents selling — honeypot detected" },
  { id: 3, type: "flash_loan", target: "0x9f8e...2b3c", risk: "high", chain: "Arbitrum", time: "8 min ago", desc: "Flash loan attack pattern detected on lending protocol" },
  { id: 4, type: "whale_alert", target: "0x1a2b...3c4d", risk: "medium", chain: "Ethereum", time: "12 min ago", desc: "Large ETH transfer: 2,500 ETH moved to unknown wallet" },
  { id: 5, type: "phishing", target: "0xab12...cd34", risk: "critical", chain: "Ethereum", time: "18 min ago", desc: "Known phishing contract mimicking Uniswap Router" },
  { id: 6, type: "oracle_manipulation", target: "0x56ef...78gh", risk: "high", chain: "Base", time: "25 min ago", desc: "Price oracle manipulation attempt detected" },
  { id: 7, type: "fake_token", target: "0xdead...beef", risk: "medium", chain: "Arbitrum", time: "31 min ago", desc: "Fake USDC token deployed — possible scam" },
  { id: 8, type: "whale_alert", target: "0x8765...4321", risk: "low", chain: "Ethereum", time: "45 min ago", desc: "Whale accumulated 50,000 LINK tokens" },
];

const riskColors = {
  critical: "bg-red-500/10 text-red-500 border-red-500/20",
  high: "bg-orange-500/10 text-orange-500 border-orange-500/20",
  medium: "bg-amber-500/10 text-amber-500 border-amber-500/20",
  low: "bg-green-500/10 text-green-500 border-green-500/20",
};

const typeIcons = {
  rug_pull: "💸",
  honeypot: "🍯",
  flash_loan: "⚡",
  whale_alert: "🐋",
  phishing: "🎣",
  oracle_manipulation: "📊",
  fake_token: "🪙",
};

export default function MonitorPage() {
  const [threats, setThreats] = useState(mockThreats);
  const [filter, setFilter] = useState("all");

  const filtered = filter === "all" ? threats : threats.filter(t => t.risk === filter);

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">🛡️ Threat Monitor</h1>
        <p className="text-zinc-500">Real-time DeFi threat detection powered by MiMo AI</p>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Active Threats", value: "7", color: "text-red-500" },
          { label: "Scanned Today", value: "3,847", color: "text-blue-500" },
          { label: "Blocked", value: "42", color: "text-green-500" },
          { label: "Protected Value", value: "$8.4M", color: "text-amber-500" },
        ].map(s => (
          <div key={s.label} className="glass rounded-xl p-4 text-center">
            <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
            <div className="text-xs text-zinc-500">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex gap-3">
        {["all", "critical", "high", "medium", "low"].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm transition ${
              filter === f ? "bg-orange-500 text-white" : "glass text-zinc-400 hover:text-white"
            }`}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Threat Feed */}
      <div className="space-y-3">
        {filtered.map(t => (
          <div key={t.id} className={`glass rounded-xl p-5 border ${riskColors[t.risk]?.split(" ").pop() || ""}`}>
            <div className="flex items-start justify-between">
              <div className="flex gap-3">
                <span className="text-2xl">{typeIcons[t.type] || "⚠️"}</span>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold">{t.type.replace(/_/g, " ").toUpperCase()}</span>
                    <span className={`px-2 py-0.5 rounded-full text-xs border ${riskColors[t.risk]}`}>
                      {t.risk}
                    </span>
                    <span className="text-xs text-zinc-600">{t.chain}</span>
                  </div>
                  <div className="text-sm text-zinc-400 mt-1">{t.desc}</div>
                  <div className="text-xs text-zinc-600 mt-1 font-mono">{t.target}</div>
                </div>
              </div>
              <div className="text-xs text-zinc-600 shrink-0">{t.time}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center text-sm text-zinc-600">
        🤖 All threats analyzed by Xiaomi MiMo V2.5 Pro | Auto-refresh every 5s
      </div>
    </div>
  );
}
