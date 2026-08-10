import { create } from 'zustand'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatState {
  messages: Message[]
  isLoading: boolean
  reasoningMode: string
  addMessage: (message: Message) => void
  setLoading: (loading: boolean) => void
  setReasoningMode: (mode: string) => void
  clearMessages: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,
  reasoningMode: 'normal',
  
  addMessage: (message) => set((state) => ({
    messages: [...state.messages, message]
  })),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setReasoningMode: (mode) => set({ reasoningMode: mode }),
  
  clearMessages: () => set({ messages: [] })
}))

interface AppState {
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  toggleSidebar: () => void
}

export const useAppStore = create<AppState>((set) => ({
  sidebarOpen: true,
  
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen }))
}))
