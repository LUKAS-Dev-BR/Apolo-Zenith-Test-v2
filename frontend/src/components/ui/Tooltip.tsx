import React, { useState, useRef, useEffect } from 'react'

interface TooltipProps {
  content: string
  children: React.ReactNode
  position?: 'top' | 'bottom' | 'left' | 'right'
}

export function Tooltip({ content, children, position = 'top' }: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false)
  const tooltipRef = useRef<HTMLDivElement>(null)

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2'
  }

  useEffect(() => {
    const handleMouseEnter = () => setIsVisible(true)
    const handleMouseLeave = () => setIsVisible(false)

    const element = tooltipRef.current
    if (element) {
      element.addEventListener('mouseenter', handleMouseEnter)
      element.addEventListener('mouseleave', handleMouseLeave)
    }

    return () => {
      if (element) {
        element.removeEventListener('mouseenter', handleMouseEnter)
        element.removeEventListener('mouseleave', handleMouseLeave)
      }
    }
  }, [])

  return (
    <div ref={tooltipRef} className="relative inline-block">
      {children}
      
      {isVisible && (
        <div 
          className={`absolute z-50 px-3 py-2 bg-canvas-card border border-hairline rounded-lg font-body-sm text-ink whitespace-nowrap animate-fade-in ${positionClasses[position]}`}
        >
          {content}
        </div>
      )}
    </div>
  )
}
