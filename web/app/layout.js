import './globals.css'

export const metadata = {
  title: 'MiMoGuard — DeFi Multi-Agent Platform',
  description: 'DeFi Multi-Agent Intelligence Platform powered by Xiaomi MiMo AI',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0a0a0f] text-zinc-100">
        <nav className="border-b border-zinc-800 bg-[#0a0a0f]/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            <a href="/" className="flex items-center gap-2 text-xl font-bold">
              🛡️ <span className="text-orange-500">MiMo</span>Guard
            </a>
            <div className="flex gap-6 text-sm">
              <a href="/" className="hover:text-orange-500 transition">Dashboard</a>
              <a href="/swap" className="hover:text-orange-500 transition">Swap</a>
              <a href="/audit" className="hover:text-orange-500 transition">Audit</a>
              <a href="/monitor" className="hover:text-orange-500 transition">Monitor</a>
            </div>
            <div className="text-xs text-zinc-500">Powered by MiMo V2.5 Pro</div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}
