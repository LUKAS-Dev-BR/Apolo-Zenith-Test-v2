import React from 'react'
import { IconButton } from './Components'

interface AlertProps {
  type?: 'info' | 'success' | 'warning' | 'error'
  title?: string
  children: React.ReactNode
  closable?: boolean
  onClose?: () => void
  className?: string
}

export function Alert({ type = 'info', title, children, closable = false, onClose, className = '' }: AlertProps) {
  const typeStyles = {
    info: 'bg-blue-900/30 border-blue-500 text-blue-200',
    success: 'bg-green-900/30 border-green-500 text-green-200',
    warning: 'bg-yellow-900/30 border-yellow-500 text-yellow-200',
    error: 'bg-red-900/30 border-red-500 text-red-200'
  }

  const typeIcons = {
    info: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 16v-4M12 8h.01" />
      </svg>
    ),
    success: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22,4 12,14.01 9,11.01" />
      </svg>
    ),
    warning: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
    ),
    error: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="15" y1="9" x2="9" y2="15" />
        <line x1="9" y1="9" x2="15" y2="15" />
      </svg>
    )
  }

  return (
    <div className={`flex items-start gap-3 p-4 rounded-lg border ${typeStyles[type]} ${className}`}>
      <div className="flex-shrink-0 mt-0.5">
        {typeIcons[type]}
      </div>
      
      <div className="flex-1 min-w-0">
        {title && (
          <h4 className="font-body-md font-medium mb-1">{title}</h4>
        )}
        <div className="font-body-sm">{children}</div>
      </div>
      
      {closable && onClose && (
        <IconButton onClick={onClose} className="flex-shrink-0 mt-0.5">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </IconButton>
      )}
    </div>
  )
}
