import React, { useState, createContext, useContext } from 'react'

interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

interface TabsProps {
  defaultValue: string
  children: React.ReactNode
  className?: string
}

export function Tabs({ defaultValue, children, className = '' }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultValue)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={className}>
        {children}
      </div>
    </TabsContext.Provider>
  )
}

interface TabListProps {
  children: React.ReactNode
  className?: string
}

export function TabList({ children, className = '' }: TabListProps) {
  return (
    <div className={`flex border-b border-hairline ${className}`}>
      {children}
    </div>
  )
}

interface TabTriggerProps {
  value: string
  children: React.ReactNode
  className?: string
}

export function TabTrigger({ value, children, className = '' }: TabTriggerProps) {
  const context = useContext(TabsContext)
  
  if (!context) {
    throw new Error('TabTrigger must be used within Tabs')
  }

  const { activeTab, setActiveTab } = context
  const isActive = activeTab === value

  return (
    <button
      className={`px-4 py-3 font-body-sm transition-colors ${
        isActive 
          ? 'text-ink border-b-2 border-ink' 
          : 'text-body-mid hover:text-ink'
      } ${className}`}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

interface TabContentProps {
  value: string
  children: React.ReactNode
  className?: string
}

export function TabContent({ value, children, className = '' }: TabContentProps) {
  const context = useContext(TabsContext)
  
  if (!context) {
    throw new Error('TabContent must be used within Tabs')
  }

  const { activeTab } = context

  if (activeTab !== value) {
    return null
  }

  return (
    <div className={`py-4 ${className}`}>
      {children}
    </div>
  )
}
