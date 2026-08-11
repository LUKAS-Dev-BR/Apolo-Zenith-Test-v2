

interface AvatarProps {
  src?: string
  alt?: string
  fallback?: string
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function Avatar({ src, alt, fallback, size = 'md', className = '' }: AvatarProps) {
  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base'
  }

  if (src) {
    return (
      <img
        src={src}
        alt={alt || ''}
        className={`rounded-full object-cover ${sizeClasses[size]} ${className}`}
      />
    )
  }

  return (
    <div 
      className={`rounded-full bg-canvas-mid flex items-center justify-center font-body-sm text-ink ${sizeClasses[size]} ${className}`}
    >
      {fallback || '?'}
    </div>
  )
}

interface AvatarGroupProps {
  avatars: Array<{ src?: string; fallback?: string }>
  max?: number
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function AvatarGroup({ avatars, max = 3, size = 'md', className = '' }: AvatarGroupProps) {
  const visibleAvatars = avatars.slice(0, max)
  const remaining = avatars.length - max

  return (
    <div className={`flex -space-x-2 ${className}`}>
      {visibleAvatars.map((avatar, index) => (
        <Avatar
          key={index}
          src={avatar.src}
          fallback={avatar.fallback}
          size={size}
          className="border-2 border-canvas"
        />
      ))}
      
      {remaining > 0 && (
        <div 
          className={`rounded-full bg-canvas-mid flex items-center justify-center font-body-sm text-ink border-2 border-canvas ${size === 'sm' ? 'w-8 h-8 text-xs' : size === 'md' ? 'w-10 h-10 text-sm' : 'w-12 h-12 text-base'}`}
        >
          +{remaining}
        </div>
      )}
    </div>
  )
}
