"use client"

import React, { useEffect, useRef, useState } from 'react'
import { Terminal as TerminalIcon, Activity, ArrowUpRight, ArrowDownRight, ShieldAlert, Wifi } from 'lucide-react'
import { useStore, TradeSignal } from '@/lib/store/useStore'
import { cn } from '@/lib/utils'

export default function Terminal() {
    const { signals, setSignals, isConnected, setConnected } = useStore()
    const [logs, setLogs] = useState<string[]>([])
    const logsEndRef = useRef<HTMLDivElement>(null)

    // Auto-scroll logs
    useEffect(() => {
        logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [logs])

    // Connect to Real Backend
    useEffect(() => {
        setConnected(true)

        const fetchSignals = async () => {
            try {
                // Use Next.js Proxy path (bypasses CORS)
                const res = await fetch('/api/python/signals/dashboard')
                if (res.ok) {
                    const data = await res.json()
                    // Update global store
                    // we can use the setSignals we destructured, but inside async sometimes clojures are tricky
                    // safest to just call setSignals from the closure if valid
                    setSignals(data)
                    setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Sync: ${data.length} active signals`].slice(-20))
                }
            } catch (e) {
                setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] Connection Error: Retrying...`].slice(-20))
            }
        }

        // Initial Fetch
        fetchSignals()

        // Poll every 5s
        const interval = setInterval(fetchSignals, 5000)

        return () => clearInterval(interval)
    }, [setConnected, setSignals])

    return (
        <div className="flex h-screen w-full flex-col bg-white text-black font-mono text-sm">
            {/* Header */}
            <header className="flex items-center justify-between border-b border-black px-4 py-2">
                <div className="flex items-center gap-2">
                    <TerminalIcon className="h-5 w-5" />
                    <h1 className="text-lg font-bold tracking-tight">ANTIGRAVITY // ENGINE</h1>
                </div>
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                        <span className="text-xs uppercase text-gray-500">Status</span>
                        <div className={`h-2 w-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                    </div>
                    <span className="text-xs text-gray-400">v1.0.0-rc1</span>
                </div>
            </header>

            {/* Main Grid */}
            <div className="grid flex-1 grid-cols-12 divide-x divide-black">
                {/* Left Panel: Signal Feed */}
                <div className="col-span-4 flex flex-col">
                    <div className="border-b border-black bg-black text-white px-3 py-1 text-xs uppercase font-semibold">
                        Signal Feed
                    </div>
                    <div className="flex-1 overflow-auto p-0">
                        {signals.length === 0 ? (
                            <div className="p-4 text-gray-400">No active signals...</div>
                        ) : (
                            signals.map((sig, idx) => (
                                <SignalCard key={idx} signal={sig} />
                            ))
                        )}
                    </div>
                </div>

                {/* Center Panel: Analytics */}
                <div className="col-span-5 flex flex-col">
                    <div className="border-b border-black bg-black text-white px-3 py-1 text-xs uppercase font-semibold">
                        Market Depth / Unlock Analytics
                    </div>
                    <div className="flex-1 p-4">
                        <div className="border border-dashed border-gray-300 p-8 flex items-center justify-center h-full">
                            <span className="text-gray-400">Chart Visualization Area</span>
                            {/* Integration point for Lightweight Charts */}
                        </div>
                    </div>
                </div>

                {/* Right Panel: Event Log / Onchain */}
                <div className="col-span-3 flex flex-col bg-gray-50">
                    <div className="border-b border-black bg-black text-white px-3 py-1 text-xs uppercase font-semibold">
                        System Log
                    </div>
                    <div className="flex-1 overflow-auto p-2 font-mono text-xs">
                        {logs.map((log, i) => (
                            <div key={i} className="mb-1">{log}</div>
                        ))}
                        <div ref={logsEndRef} />
                    </div>
                </div>
            </div>
        </div>
    )
}

function SignalCard({ signal }: { signal: TradeSignal }) {
    const isShort = signal.signal === 'SHORT'
    const isLong = signal.signal === 'LONG_AFTER_DUMP'

    return (
        <div className="border-b border-gray-200 p-3 hover:bg-gray-50">
            <div className="flex justify-between items-start mb-2">
                <span className="font-bold text-lg">{signal.token}</span>
                <span className={cn(
                    "px-2 py-0.5 text-xs font-bold border",
                    isShort ? "border-black bg-black text-white" : "border-gray-400 text-gray-500"
                )}>
                    {signal.signal}
                </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs mb-2">
                <div>
                    <span className="text-gray-500 block">UIS Score</span>
                    <span className="font-mono">{signal.uis_score}</span>
                </div>
                <div>
                    <span className="text-gray-500 block">Confidence</span>
                    <span className="font-mono">{signal.confidence}%</span>
                </div>
            </div>

            <div className="text-xs text-gray-600 border-l-2 border-gray-300 pl-2">
                {signal.reason}
            </div>
        </div>
    )
}
