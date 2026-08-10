import { useState } from 'react'
import Chat from './components/chat/Chat'
import { Header } from './components/ui/Header'
import { Sidebar } from './components/ui/Sidebar'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex h-screen bg-canvas text-ink">
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="flex-1 flex flex-col min-w-0">
        <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
        
        <main className="flex-1 overflow-hidden">
          <Chat />
        </main>
      </div>
    </div>
  )
}

export default App
