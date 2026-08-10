import React from 'react'

interface ListProps<T> {
  items: T[]
  renderItem: (item: T, index: number) => React.ReactNode
  keyExtractor: (item: T) => string
  emptyMessage?: string
  className?: string
}

export function List<T>({ items, renderItem, keyExtractor, emptyMessage = 'Nenhum item encontrado', className = '' }: ListProps<T>) {
  if (items.length === 0) {
    return (
      <div className={`card text-center py-8 ${className}`}>
        <p className="font-body-sm text-mute">{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {items.map((item, index) => (
        <div key={keyExtractor(item)}>
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  )
}

interface ListItemProps {
  children: React.ReactNode
  onClick?: () => void
  active?: boolean
  className?: string
}

export function ListItem({ children, onClick, active = false, className = '' }: ListItemProps) {
  return (
    <div
      className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${
        active 
          ? 'bg-canvas-soft border border-hairline' 
          : 'hover:bg-canvas-soft cursor-pointer'
      } ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  )
}

interface ListItemIconProps {
  children: React.ReactNode
  className?: string
}

export function ListItemIcon({ children, className = '' }: ListItemIconProps) {
  return (
    <div className={`flex-shrink-0 w-8 h-8 rounded-full bg-canvas-mid flex items-center justify-center ${className}`}>
      {children}
    </div>
  )
}

interface ListItemContentProps {
  primary: string
  secondary?: string
  className?: string
}

export function ListItemContent({ primary, secondary, className = '' }: ListItemContentProps) {
  return (
    <div className={`flex-1 min-w-0 ${className}`}>
      <p className="font-body-sm text-ink truncate">{primary}</p>
      {secondary && (
        <p className="font-caption-mono-sm text-mute truncate">{secondary}</p>
      )}
    </div>
  )
}

interface ListItemActionsProps {
  children: React.ReactNode
  className?: string
}

export function ListItemActions({ children, className = '' }: ListItemActionsProps) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {children}
    </div>
  )
}
