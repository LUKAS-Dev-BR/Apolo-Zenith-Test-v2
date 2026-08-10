import React, { useState, useRef, useEffect } from 'react'

interface DropdownProps {
  trigger: React.ReactNode
  children: React.ReactNode
  align?: 'start' | 'center' | 'end'
  className?: string
}

export function Dropdown({ trigger, children, align = 'start', className = '' }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const alignClasses = {
    start: 'left-0',
    center: 'left-1/2 -translate-x-1/2',
    end: 'right-0'
  }

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  return (
    <div ref={dropdownRef} className="relative inline-block">
      <div onClick={() => setIsOpen(!isOpen)}>
        {trigger}
      </div>
      
      {isOpen && (
        <div 
          className={`absolute top-full mt-2 z-50 bg-canvas-card border border-hairline rounded-lg shadow-lg min-w-[200px] ${alignClasses[align]} ${className}`}
        >
          {children}
        </div>
      )}
    </div>
  )
}

interface DropdownItemProps {
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  className?: string
}

export function DropdownItem({ children, onClick, disabled = false, className = '' }: DropdownItemProps) {
  return (
    <button
      className={`w-full text-left px-4 py-2 font-body-sm text-ink hover:bg-canvas-soft transition-colors ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      } ${className}`}
      onClick={() => {
        if (!disabled && onClick) {
          onClick()
        }
      }}
      disabled={disabled}
    >
      {children}
    </button>
  )
}

interface DropdownSeparatorProps {
  className?: string
}

export function DropdownSeparator({ className = '' }: DropdownSeparatorProps) {
  return <div className={`border-t border-hairline my-1 ${className}`} />
}
