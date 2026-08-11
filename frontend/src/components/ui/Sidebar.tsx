import React from 'react'
import { Eyebrow, Divider } from './Components'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
}

export function Sidebar({ isOpen, onToggle }: SidebarProps) {
  return (
    <>
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onToggle}
        />
      )}
      
      <aside
        className={`fixed md:static inset-y-0 left-0 z-50 w-64 bg-canvas border-r border-hairline transform transition-transform duration-300 ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0 md:w-0 md:overflow-hidden'
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="p-4 border-b border-hairline">
            <Eyebrow>Navegação</Eyebrow>
          </div>

          <nav className="flex-1 p-4 space-y-1">
            <SidebarItem 
              icon={
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              }
              label="Nova Conversa"
              active
            />
            
            <SidebarItem 
              icon={
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                  <polyline points="14,2 14,8 20,8" />
                </svg>
              }
              label="Documentos"
            />
            
            <SidebarItem 
              icon={
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <polyline points="21,15 16,10 5,21" />
                </svg>
              }
              label="Galeria"
            />
          </nav>

          <Divider className="mx-4" />

          <div className="p-4 space-y-2">
            <Eyebrow>Modo de Raciocínio</Eyebrow>
            
            <select className="input-field w-full text-sm">
              <option value="normal">Normal</option>
              <option value="medium">Médio</option>
              <option value="high">Alto</option>
              <option value="very_high">Muito Alto</option>
              <option value="ultra_high">Ultra Alto</option>
              <option value="ultra_mega_high">Ultra Mega Alto</option>
            </select>
          </div>

          <Divider className="mx-4" />

          <div className="p-4">
            <div className="card-soft p-3">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-canvas-mid flex items-center justify-center">
                  <span className="font-body-sm text-ink">AZ</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-body-sm text-ink truncate">Apolo Zenith 1.9</p>
                  <p className="font-caption-mono-sm text-mute">IA Multimodal</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

interface SidebarItemProps {
  icon: React.ReactNode
  label: string
  active?: boolean
}

function SidebarItem({ icon, label, active = false }: SidebarItemProps) {
  return (
    <button
      className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
        active 
          ? 'bg-canvas-soft text-ink' 
          : 'text-body-mid hover:text-ink hover:bg-canvas-soft'
      }`}
    >
      {icon}
      <span className="font-body-sm truncate">{label}</span>
    </button>
  )
}
