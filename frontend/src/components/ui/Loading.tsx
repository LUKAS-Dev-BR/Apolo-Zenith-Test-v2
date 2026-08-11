

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function LoadingSpinner({ size = 'md', className = '' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  }

  return (
    <div className={`${sizeClasses[size]} animate-spin ${className}`}>
      <svg
        className="text-body-mid"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        />
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </div>
  )
}

interface LoadingDotsProps {
  className?: string
}

export function LoadingDots({ className = '' }: LoadingDotsProps) {
  return (
    <div className={`flex items-center gap-1 ${className}`}>
      <div className="w-2 h-2 bg-body-mid rounded-full animate-pulse-subtle" />
      <div className="w-2 h-2 bg-body-mid rounded-full animate-pulse-subtle" style={{ animationDelay: '0.2s' }} />
      <div className="w-2 h-2 bg-body-mid rounded-full animate-pulse-subtle" style={{ animationDelay: '0.4s' }} />
    </div>
  )
}

interface LoadingBarProps {
  progress?: number
  className?: string
}

export function LoadingBar({ progress = 0, className = '' }: LoadingBarProps) {
  return (
    <div className={`w-full h-1 bg-canvas-mid rounded-full overflow-hidden ${className}`}>
      <div 
        className="h-full bg-body-mid transition-all duration-300"
        style={{ width: `${progress}%` }}
      />
    </div>
  )
}
