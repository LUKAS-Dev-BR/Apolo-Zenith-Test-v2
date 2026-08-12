import { Eyebrow, Divider } from './Components'
import { User, Conversation } from '../../App'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
  user: User
  conversations: Conversation[]
  activeConversation: number | null
  onSelectConversation: (id: number) => void
  onNewConversation: () => void
  onDeleteConversation: (id: number) => void
  activeView: 'chat' | 'documents' | 'gallery'
  onSelectView: (view: 'chat' | 'documents' | 'gallery') => void
  onLogout: () => void
}

export function Sidebar({
  isOpen, onToggle, user, conversations, activeConversation,
  onSelectConversation, onNewConversation, onDeleteConversation,
  activeView, onSelectView, onLogout
}: SidebarProps) {
  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 z-40 md:hidden" onClick={onToggle} />
      )}
      
      <aside className={`fixed md:static inset-y-0 left-0 z-50 w-72 bg-canvas border-r border-hairline transform transition-transform duration-300 ${
        isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0 md:w-0 md:overflow-hidden'
      }`}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-4 border-b border-hairline">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-body-sm text-ink">Apolo Zenith</span>
                <span className="font-caption-mono-sm text-mute">1.9</span>
              </div>
              <button onClick={onToggle} className="text-mute hover:text-ink transition-colors md:hidden">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* New Conversation Button */}
          <div className="p-3">
            <button onClick={onNewConversation} className="btn-primary w-full">
              + Nova Conversa
            </button>
          </div>

          {/* Nav Items */}
          <div className="px-3 space-y-1">
            <button
              onClick={() => onSelectView('chat')}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                activeView === 'chat' ? 'bg-canvas-soft text-ink' : 'text-body-mid hover:text-ink hover:bg-canvas-soft'
              }`}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <span className="font-body-sm">Chat</span>
            </button>
            <button
              onClick={() => onSelectView('documents')}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                activeView === 'documents' ? 'bg-canvas-soft text-ink' : 'text-body-mid hover:text-ink hover:bg-canvas-soft'
              }`}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14,2 14,8 20,8" />
              </svg>
              <span className="font-body-sm">Documentos</span>
            </button>
            <button
              onClick={() => onSelectView('gallery')}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                activeView === 'gallery' ? 'bg-canvas-soft text-ink' : 'text-body-mid hover:text-ink hover:bg-canvas-soft'
              }`}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <circle cx="8.5" cy="8.5" r="1.5" />
                <polyline points="21,15 16,10 5,21" />
              </svg>
              <span className="font-body-sm">Galeria</span>
            </button>
          </div>

          <Divider className="mx-3 my-3" />

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto px-3">
            <Eyebrow className="mb-2">Conversas</Eyebrow>
            <div className="space-y-1">
              {conversations.length === 0 && (
                <p className="font-body-sm text-mute py-2">Nenhuma conversa ainda</p>
              )}
              {conversations.map(conv => (
                <div
                  key={conv.id}
                  onClick={() => onSelectConversation(conv.id)}
                  className={`group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                    activeConversation === conv.id
                      ? 'bg-canvas-soft text-ink'
                      : 'text-body-mid hover:text-ink hover:bg-canvas-soft'
                  }`}
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="flex-shrink-0">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                  </svg>
                  <span className="font-body-sm truncate flex-1">{conv.title}</span>
                  <button
                    onClick={(e) => { e.stopPropagation(); onDeleteConversation(conv.id) }}
                    className="opacity-0 group-hover:opacity-100 text-mute hover:text-red-400 transition-all"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          </div>

          <Divider className="mx-3" />

          {/* User Info */}
          <div className="p-3">
            <div className="card-soft p-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-accent-dusk flex items-center justify-center">
                  <span className="font-body-sm text-ink">{user.username[0].toUpperCase()}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-body-sm text-ink truncate">{user.username}</p>
                  <p className="font-caption-mono-sm text-mute">Online</p>
                </div>
                <button onClick={onLogout} className="text-mute hover:text-ink transition-colors" title="Sair">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
