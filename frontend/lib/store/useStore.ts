import { create } from 'zustand'

export type SignalType = 'SHORT' | 'AVOID' | 'LONG_AFTER_DUMP'

export interface TradeSignal {
    token: string
    signal: SignalType
    uis_score: number
    confidence: number
    expected_move_pct: number
    reason: string
}

interface AppState {
    signals: TradeSignal[]
    setSignals: (signals: TradeSignal[]) => void
    addSignal: (signal: TradeSignal) => void
    isConnected: boolean
    setConnected: (status: boolean) => void
}

export const useStore = create<AppState>((set) => ({
    signals: [],
    setSignals: (signals) => set({ signals }),
    addSignal: (signal) => set((state) => ({ signals: [signal, ...state.signals].slice(0, 50) })),
    isConnected: false,
    setConnected: (status) => set({ isConnected: status }),
}))
