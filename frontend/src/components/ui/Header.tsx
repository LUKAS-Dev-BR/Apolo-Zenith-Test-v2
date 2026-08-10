import React from 'react'
import { Button, IconButton } from './Components'

interface HeaderProps {
  onMenuToggle: () => void
}

export function Header({ onMenuToggle }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-canvas border-b border-hairline">
      <div className="flex items-center justify-between px-4 md:px-6 py-3">
        <div className="flex items-center gap-4">
          <IconButton onClick={onMenuToggle} className="md:hidden">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 12h18M3 6h18M3 18h18" />
            </svg>
          </IconButton>
          
          <div className="flex items-center gap-2">
            <span className="font-body-sm text-ink tracking-wider uppercase">Apolo Zenith</span>
            <span className="font-caption-mono-sm text-mute">1.9</span>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-6">
          <a href="#" className="font-body-sm text-ink hover:text-ink-hover transition-colors">
            Chat
          </a>
          <a href="#" className="font-body-sm text-body-mid hover:text-ink transition-colors">
            Motores
          </a>
          <a href="#" className="font-body-sm text-body-mid hover:text-ink transition-colors">
            Agentes
          </a>
          <a href="#" className="font-body-sm text-body-mid hover:text-ink transition-colors">
            API
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <Button variant="outline-sm" className="hidden sm:block">
            Documentação
          </Button>
          <Button variant="primary">
            Iniciar
          </Button>
        </div>
      </div>
    </header>
  )
}
