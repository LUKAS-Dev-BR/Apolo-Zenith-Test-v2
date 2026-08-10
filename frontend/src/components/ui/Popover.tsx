import React, { useState, useRef, useEffect } from 'react'

interface PopoverProps {
  trigger: React.ReactNode
  children: React.ReactNode
  align?: 'start' | 'center' | 'end'
  side?: 'top' | 'bottom' | 'left' | 'right'
  className?: string
}

export function Popover({ trigger, children, align = 'center', side = 'bottom', className = '' }: PopoverProps) {
  const [isOpen, setIsOpen] = useState(false)
  const popoverRef = useRef<HTMLDivElement>(null)

  const alignClasses = {
    start: 'left-0',
    center: 'left-1/2 -translate-x-1/2',
    end: 'right-0'
  }

  const sideClasses = {
    top: 'bottom-full mb-2',
    bottom: 'top-full mt-2',
    left: 'right-full mr-2',
    right: 'left-full ml-2'
  }

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(event.target as Node)) {
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
    <div ref={popoverRef} className="relative inline-block">
      <div onClick={() => setIsOpen(!isOpen)}>
        {trigger}
      </div>
      
      {isOpen && (
        <div 
          className={`absolute z-50 bg-canvas-card border border-hairline rounded-lg shadow-lg ${sideClasses[side]} ${alignClasses[align]} ${className}`}
        >
          {children}
        </div>
      )}
    </div>
  )
}

interface PopoverContentProps {
  children: React.ReactNode
  className?: string
}

export function PopoverContent({ children, className = '' }: PopoverContentProps) {
  return (
    <div className={`p-4 ${className}`}>
      {children}
    </div>
  )
}
