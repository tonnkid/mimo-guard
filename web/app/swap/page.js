"use client";

import { useState } from "react";

const tokens = ["ETH", "BTC", "USDC", "USDT", "DAI", "LINK", "UNI", "AAVE", "ARB"];

export default function SwapPage() {
  const [tokenIn, setTokenIn] = useState("ETH");
  const [tokenOut, setTokenOut] = useState("USDC");
  const [amount, setAmount] = useState("1.0");
  const [rates, setRates] = useState(null);
  const [loading, setLoading] = useState(false);

  const getBestRate = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      const baseRate = tokenIn === "ETH" ? 1850 : 1;
      setRates([
        { dex: "Uniswap V3", output: (parseFloat(amount) * baseRate * 0.997 * 1.012).toFixed(2), impact: "0.12%", gas: "$4.50", liquidity: "$45.2M" },
        { dex: "SushiSwap", output: (parseFloat(amount) * baseRate * 0.997 * 0.994).toFixed(2), impact: "0.18%", gas: "$3.80", liquidity: "$12.8M" },
        { dex: "PancakeSwap", output: (parseFloat(amount) * baseRate * 0.9975 * 1.003).toFixed(2), impact: "0.08%", gas: "$2.10", liquidity: "$28.5M" },
      ]);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">🔍 Token Swap</h1>
        <p className="text-zinc-500">Find the best rates across multiple DEXes</p>
      </div>

      {/* Swap Form */}
      <div className="glass rounded-xl p-8 space-y-6">
        <div>
          <label className="text-sm text-zinc-500 mb-2 block">From</label>
          <div className="flex gap-3">
            <select value={tokenIn} onChange={e => setTokenIn(e.target.value)}
              className="bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-3 text-lg focus:border-orange-500 outline-none">
              {tokens.map(t => <option key={t}>{t}</option>)}
            </select>
            <input type="number" value={amount} onChange={e => setAmount(e.target.value)}
              className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-3 text-lg focus:border-orange-500 outline-none"
              placeholder="0.0" step="0.1" />
          </div>
        </div>

        <div className="flex justify-center">
          <button onClick={() => { const t = tokenIn; setTokenIn(tokenOut); setTokenOut(t); }}
            className="w-10 h-10 rounded-full bg-zinc-800 border border-zinc-700 hover:border-orange-500 transition flex items-center justify-center">
            ↕
          </button>
        </div>

        <div>
          <label className="text-sm text-zinc-500 mb-2 block">To</label>
          <select value={tokenOut} onChange={e => setTokenOut(e.target.value)}
            className="w-full bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-3 text-lg focus:border-orange-500 outline-none">
            {tokens.filter(t => t !== tokenIn).map(t => <option key={t}>{t}</option>)}
          </select>
        </div>

        <button onClick={getBestRate} disabled={loading}
          className="w-full py-4 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-bold text-lg transition disabled:opacity-50">
          {loading ? "⏳ Finding best rate..." : "🔍 Get Best Rate"}
        </button>
      </div>

      {/* Results */}
      {rates && (
        <div className="space-y-4">
          <h2 className="text-xl font-bold">📊 DEX Comparison</h2>
          {rates.map((r, i) => (
            <div key={r.dex} className={`glass rounded-xl p-6 ${i === 0 ? "border-green-500/30 glow-orange" : ""}`}>
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-bold text-lg">{r.dex}</div>
                  <div className="text-sm text-zinc-500">Impact: {r.impact} | Gas: {r.gas} | Liquidity: {r.liquidity}</div>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${i === 0 ? "text-green-500" : ""}`}>{r.output} {tokenOut}</div>
                  {i === 0 && <span className="text-xs text-green-500">✨ Best Rate</span>}
                </div>
              </div>
            </div>
          ))}
          <div className="glass rounded-xl p-4 text-center text-sm text-zinc-500">
            🤖 Powered by Xiaomi MiMo AI — Analysis by MiMo-V2.5-Pro
          </div>
        </div>
      )}
    </div>
  );
}
