import React, { useState, createContext, useContext } from 'react'

interface AccordionContextValue {
  openItems: string[]
  toggleItem: (item: string) => void
}

const AccordionContext = createContext<AccordionContextValue | undefined>(undefined)

interface AccordionProps {
  children: React.ReactNode
  type?: 'single' | 'multiple'
  className?: string
}

export function Accordion({ children, type = 'single', className = '' }: AccordionProps) {
  const [openItems, setOpenItems] = useState<string[]>([])

  const toggleItem = (item: string) => {
    if (type === 'single') {
      setOpenItems(prev => prev.includes(item) ? [] : [item])
    } else {
      setOpenItems(prev => 
        prev.includes(item) 
          ? prev.filter(i => i !== item)
          : [...prev, item]
      )
    }
  }

  return (
    <AccordionContext.Provider value={{ openItems, toggleItem }}>
      <div className={`space-y-2 ${className}`}>
        {children}
      </div>
    </AccordionContext.Provider>
  )
}

interface AccordionItemProps {
  value: string
  children: React.ReactNode
  className?: string
}

export function AccordionItem({ value, children, className = '' }: AccordionItemProps) {
  return (
    <div className={`card ${className}`}>
      {children}
    </div>
  )
}

interface AccordionTriggerProps {
  value: string
  children: React.ReactNode
  className?: string
}

export function AccordionTrigger({ value, children, className = '' }: AccordionTriggerProps) {
  const context = useContext(AccordionContext)
  
  if (!context) {
    throw new Error('AccordionTrigger must be used within Accordion')
  }

  const { openItems, toggleItem } = context
  const isOpen = openItems.includes(value)

  return (
    <button
      className={`w-full flex items-center justify-between p-4 text-left ${className}`}
      onClick={() => toggleItem(value)}
    >
      <span className="font-body-md text-ink">{children}</span>
      <svg 
        width="20" 
        height="20" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        strokeWidth="2"
        className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`}
      >
        <path d="M6 9l6 6 6-6" />
      </svg>
    </button>
  )
}

interface AccordionContentProps {
  value: string
  children: React.ReactNode
  className?: string
}

export function AccordionContent({ value, children, className = '' }: AccordionContentProps) {
  const context = useContext(AccordionContext)
  
  if (!context) {
    throw new Error('AccordionContent must be used within Accordion')
  }

  const { openItems } = context
  const isOpen = openItems.includes(value)

  if (!isOpen) {
    return null
  }

  return (
    <div className={`px-4 pb-4 ${className}`}>
      <div className="font-body-sm text-body">
        {children}
      </div>
    </div>
  )
}
