import { useState, useEffect } from 'react'
import Chat from './components/chat/Chat'
import { Header } from './components/ui/Header'
import { Sidebar } from './components/ui/Sidebar'
import Login from './components/auth/Login'

export interface User {
  user_id: number
  username: string
}

export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count: number
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversation, setActiveConversation] = useState<number | null>(null)
  const [activeView, setActiveView] = useState<'chat' | 'documents' | 'gallery'>('chat')
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    if (token && savedUser) {
      setUser(JSON.parse(savedUser))
    }
  }, [])

  useEffect(() => {
    if (user) {
      loadConversations()
    }
  }, [user, refreshKey])

  const loadConversations = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('/api/chat/conversations', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        setConversations(await res.json())
      }
    } catch (e) {
      console.error('Erro ao carregar conversas:', e)
    }
  }

  const handleLogin = (userData: User, token: string) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    setConversations([])
    setActiveConversation(null)
  }

  const handleNewConversation = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('/api/chat/conversations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ title: 'Nova Conversa' })
      })
      if (res.ok) {
        const conv = await res.json()
        setConversations(prev => [{ ...conv, message_count: 0 }, ...prev])
        setActiveConversation(conv.id)
        setActiveView('chat')
        setRefreshKey(k => k + 1)
      }
    } catch (e) {
      console.error('Erro ao criar conversa:', e)
    }
  }

  const handleSelectConversation = (convId: number) => {
    setActiveConversation(convId)
    setActiveView('chat')
  }

  const handleDeleteConversation = async (convId: number) => {
    try {
      const token = localStorage.getItem('token')
      await fetch(`/api/chat/conversations/${convId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      setConversations(prev => prev.filter(c => c.id !== convId))
      if (activeConversation === convId) {
        setActiveConversation(null)
      }
    } catch (e) {
      console.error('Erro ao deletar conversa:', e)
    }
  }

  if (!user) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="flex h-screen bg-canvas text-ink">
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        user={user}
        conversations={conversations}
        activeConversation={activeConversation}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
        activeView={activeView}
        onSelectView={setActiveView}
        onLogout={handleLogout}
      />
      
      <div className="flex-1 flex flex-col min-w-0">
        <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
        
        <main className="flex-1 overflow-hidden">
          <Chat
            conversationId={activeConversation}
            onConversationCreated={(id) => {
              setActiveConversation(id)
              setRefreshKey(k => k + 1)
            }}
          />
        </main>
      </div>
    </div>
  )
}

export default App
