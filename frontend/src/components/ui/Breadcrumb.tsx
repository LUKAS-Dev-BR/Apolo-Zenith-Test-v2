import React from 'react'

interface BreadcrumbProps {
  items: Array<{ label: string; href?: string }>
  className?: string
}

export function Breadcrumb({ items, className = '' }: BreadcrumbProps) {
  return (
    <nav className={`flex items-center gap-2 ${className}`}>
      {items.map((item, index) => (
        <React.Fragment key={index}>
          {index > 0 && (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-mute">
              <path d="M9 18l6-6-6-6" />
            </svg>
          )}
          
          {item.href ? (
            <a 
              href={item.href}
              className="font-body-sm text-body-mid hover:text-ink transition-colors"
            >
              {item.label}
            </a>
          ) : (
            <span className="font-body-sm text-ink">
              {item.label}
            </span>
          )}
        </React.Fragment>
      ))}
    </nav>
  )
}
