import React from 'react'
import { Eyebrow } from './Components'

interface FeatureCardProps {
  title: string
  description: string
  icon?: React.ReactNode
  eyebrow?: string
  className?: string
}

export function FeatureCard({ title, description, icon, eyebrow, className = '' }: FeatureCardProps) {
  return (
    <div className={`card hover:border-body-mid transition-colors ${className}`}>
      {eyebrow && (
        <Eyebrow className="mb-2 block">{eyebrow}</Eyebrow>
      )}
      
      <div className="flex items-start gap-4">
        {icon && (
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-canvas-mid flex items-center justify-center">
            {icon}
          </div>
        )}
        
        <div className="flex-1 min-w-0">
          <h3 className="font-display-xs text-ink mb-2">{title}</h3>
          <p className="font-body-sm text-body">{description}</p>
        </div>
      </div>
    </div>
  )
}

interface MediaCardProps {
  type: 'image' | 'video' | 'audio' | 'music'
  title: string
  description: string
  onClick?: () => void
  className?: string
}

export function MediaCard({ type, title, description, onClick, className = '' }: MediaCardProps) {
  const typeIcons = {
    image: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <polyline points="21,15 16,10 5,21" />
      </svg>
    ),
    video: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <polygon points="5,3 19,12 5,21,5,3" />
      </svg>
    ),
    audio: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M9 18V5l12-2v13" />
        <circle cx="6" cy="18" r="3" />
        <circle cx="18" cy="16" r="3" />
      </svg>
    ),
    music: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M9 18V5l12-2v13" />
        <circle cx="6" cy="18" r="3" />
        <circle cx="18" cy="16" r="3" />
      </svg>
    )
  }

  const typeLabels = {
    image: 'Imagem',
    video: 'Vídeo',
    audio: 'Áudio',
    music: 'Música'
  }

  return (
    <div 
      className={`card cursor-pointer hover:border-body-mid transition-colors ${className}`}
      onClick={onClick}
    >
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-canvas-mid flex items-center justify-center text-ink">
          {typeIcons[type]}
        </div>
        <div>
          <Eyebrow className="block">{typeLabels[type]}</Eyebrow>
          <h3 className="font-body-md text-ink">{title}</h3>
        </div>
      </div>
      
      <p className="font-body-sm text-body">{description}</p>
    </div>
  )
}
