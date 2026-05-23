"use client";

import { useState, useEffect } from "react";

const agents = [
  { name: "Orchestrator", icon: "🧠", model: "MiMo-V2.5-Pro", status: "online", desc: "Central coordination & event routing", tokens: "2.8B/day" },
  { name: "Swap Agent", icon: "🔍", model: "MiMo-V2.5-Pro", status: "online", desc: "Best rates across DEXes", tokens: "3.1B/day" },
  { name: "Threat Agent", icon: "🛡️", model: "MiMo-V2.5-Pro", status: "online", desc: "Scam & rug pull detection", tokens: "2.4B/day" },
  { name: "Auditor", icon: "🔬", model: "MiMo-V2.5-Pro", status: "online", desc: "4-pass contract analysis", tokens: "2.9B/day" },
];

const stats = [
  { label: "Contracts Scanned", value: "12,847", color: "text-green-500", icon: "📄" },
  { label: "Threats Blocked", value: "342", color: "text-red-500", icon: "🚨" },
  { label: "Losses Prevented", value: "$2.1M", color: "text-amber-500", icon: "💰" },
  { label: "Tokens Used", value: "15.2B", color: "text-blue-500", icon: "⚡" },
];

function AnimatedNumber({ target, duration = 2000 }) {
  const [current, setCurrent] = useState(0);
  useEffect(() => {
    const numTarget = parseFloat(target.replace(/[^0-9.]/g, ""));
    const steps = 60;
    const increment = numTarget / steps;
    let curr = 0;
    const timer = setInterval(() => {
      curr += increment;
      if (curr >= numTarget) { setCurrent(numTarget); clearInterval(timer); }
      else setCurrent(Math.floor(curr));
    }, duration / steps);
    return () => clearInterval(timer);
  }, [target, duration]);
  return <span>{typeof target === "string" && target.startsWith("$") ? "$" : ""}{current.toLocaleString()}</span>;
}

export default function Home() {
  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="text-center py-12">
        <h1 className="text-5xl font-bold mb-4">
          🛡️ <span className="text-orange-500">MiMo</span>Guard
        </h1>
        <p className="text-xl text-zinc-400 mb-2">
          DeFi Multi-Agent Intelligence Platform
        </p>
        <p className="text-sm text-zinc-600">
          基于小米 MiMo 大模型的 DeFi 多智能体安全平台
        </p>
        <div className="mt-6 flex justify-center gap-4">
          <span className="px-4 py-2 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-500 text-sm">
            ⚡ 4 AI Agents Active
          </span>
          <span className="px-4 py-2 rounded-full bg-green-500/10 border border-green-500/20 text-green-500 text-sm">
            ✅ 99.7% Uptime
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="glass rounded-xl p-6 text-center">
            <div className="text-3xl mb-2">{s.icon}</div>
            <div className={`text-3xl font-bold ${s.color}`}>
              <AnimatedNumber target={s.value} />
            </div>
            <div className="text-sm text-zinc-500 mt-1">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Agent Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-4">🤖 Agent Fleet</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((a) => (
            <div key={a.name} className="glass rounded-xl p-6 hover:border-orange-500/30 transition">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{a.icon}</span>
                  <div>
                    <div className="font-bold text-lg">{a.name}</div>
                    <div className="text-xs text-zinc-500">{a.model}</div>
                  </div>
                </div>
                <span className="flex items-center gap-1.5 text-sm text-green-500">
                  <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  Online
                </span>
              </div>
              <p className="text-zinc-400 text-sm mb-2">{a.desc}</p>
              <div className="text-xs text-zinc-600">Token usage: {a.tokens}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Activity Feed */}
      <div>
        <h2 className="text-2xl font-bold mb-4">📡 Live Activity</h2>
        <div className="glass rounded-xl p-6 space-y-3 max-h-64 overflow-y-auto">
          {[
            { time: "2s ago", msg: "🔍 Swap Agent found best rate on Uniswap: 1 ETH → 1,847.32 USDC", color: "text-blue-400" },
            { time: "15s ago", msg: "🛡️ Threat Agent flagged suspicious contract 0x7a25...f8c2 as honeypot", color: "text-red-400" },
            { time: "32s ago", msg: "🔬 Auditor completed 4-pass analysis: Contract 0x1f98...0x9d2 rated SAFE (risk: 12/100)", color: "text-green-400" },
            { time: "1m ago", msg: "🧠 Orchestrator dispatched 3 events to specialized agents", color: "text-orange-400" },
            { time: "2m ago", msg: "🔍 Swap Agent analyzed 5 DEXes for ETH→USDC swap", color: "text-blue-400" },
            { time: "3m ago", msg: "🛡️ Threat Agent detected large whale movement: 500 ETH transfer", color: "text-amber-400" },
          ].map((item, i) => (
            <div key={i} className="flex gap-3 text-sm">
              <span className="text-zinc-600 shrink-0 w-16">{item.time}</span>
              <span className={item.color}>{item.msg}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
