import React from 'react'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'default' | 'success' | 'error' | 'warning' | 'info'
  size?: 'sm' | 'md'
  className?: string
}

export function Badge({ children, variant = 'default', size = 'sm', className = '' }: BadgeProps) {
  const variantClasses = {
    default: 'bg-canvas-mid text-ink',
    success: 'bg-green-900 text-green-300',
    error: 'bg-red-900 text-red-300',
    warning: 'bg-yellow-900 text-yellow-300',
    info: 'bg-blue-900 text-blue-300'
  }

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm'
  }

  return (
    <span className={`inline-flex items-center rounded-full font-caption-mono-sm ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}>
      {children}
    </span>
  )
}

interface StatusBadgeProps {
  status: 'pending' | 'processing' | 'completed' | 'failed'
  className?: string
}

export function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  const statusConfig = {
    pending: { label: 'Pendente', variant: 'warning' as const },
    processing: { label: 'Processando', variant: 'info' as const },
    completed: { label: 'Concluído', variant: 'success' as const },
    failed: { label: 'Falhou', variant: 'error' as const }
  }

  const config = statusConfig[status]

  return (
    <Badge variant={config.variant} className={className}>
      {config.label}
    </Badge>
  )
}
