import React from 'react'

interface ProgressProps {
  value: number
  max?: number
  size?: 'sm' | 'md' | 'lg'
  showValue?: boolean
  className?: string
}

export function Progress({ value, max = 100, size = 'md', showValue = false, className = '' }: ProgressProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  
  const sizeClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3'
  }

  return (
    <div className={`w-full ${className}`}>
      <div className={`w-full bg-canvas-mid rounded-full overflow-hidden ${sizeClasses[size]}`}>
        <div 
          className="h-full bg-body-mid transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>
      
      {showValue && (
        <p className="mt-1 font-caption-mono-sm text-mute text-right">
          {Math.round(percentage)}%
        </p>
      )}
    </div>
  )
}

interface CircularProgressProps {
  value: number
  max?: number
  size?: number
  strokeWidth?: number
  showValue?: boolean
  className?: string
}

export function CircularProgress({ 
  value, 
  max = 100, 
  size = 40, 
  strokeWidth = 4, 
  showValue = false,
  className = '' 
}: CircularProgressProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100)
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (percentage / 100) * circumference

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-canvas-mid"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="text-body-mid transition-all duration-300"
        />
      </svg>
      
      {showValue && (
        <span className="absolute font-caption-mono-sm text-ink">
          {Math.round(percentage)}%
        </span>
      )}
    </div>
  )
}
