import {} from 'react'

interface SwitchProps {
  checked: boolean
  onChange: (checked: boolean) => void
  disabled?: boolean
  label?: string
  className?: string
}

export function Switch({ checked, onChange, disabled = false, label, className = '' }: SwitchProps) {
  return (
    <label className={`inline-flex items-center gap-3 cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        onClick={() => !disabled && onChange(!checked)}
        disabled={disabled}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          checked ? 'bg-body-mid' : 'bg-canvas-mid'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-ink transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
      
      {label && (
        <span className="font-body-sm text-ink">{label}</span>
      )}
    </label>
  )
}

interface CheckboxProps {
  checked: boolean
  onChange: (checked: boolean) => void
  disabled?: boolean
  label?: string
  className?: string
}

export function Checkbox({ checked, onChange, disabled = false, label, className = '' }: CheckboxProps) {
  return (
    <label className={`inline-flex items-center gap-3 cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}>
      <button
        type="button"
        role="checkbox"
        aria-checked={checked}
        onClick={() => !disabled && onChange(!checked)}
        disabled={disabled}
        className={`w-5 h-5 rounded border transition-colors flex items-center justify-center ${
          checked 
            ? 'bg-body-mid border-body-mid' 
            : 'bg-transparent border-hairline hover:border-body-mid'
        }`}
      >
        {checked && (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
            <path d="M20 6L9 17l-5-5" />
          </svg>
        )}
      </button>
      
      {label && (
        <span className="font-body-sm text-ink">{label}</span>
      )}
    </label>
  )
}

interface RadioProps {
  checked: boolean
  onChange: () => void
  disabled?: boolean
  label?: string
  name?: string
  className?: string
}

export function Radio({ checked, onChange, disabled = false, label, name, className = '' }: RadioProps) {
  return (
    <label className={`inline-flex items-center gap-3 cursor-pointer ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}>
      <button
        type="button"
        role="radio"
        aria-checked={checked}
        onClick={() => !disabled && onChange()}
        disabled={disabled}
        name={name}
        className={`w-5 h-5 rounded-full border transition-colors flex items-center justify-center ${
          checked 
            ? 'border-body-mid' 
            : 'border-hairline hover:border-body-mid'
        }`}
      >
        {checked && (
          <div className="w-2.5 h-2.5 rounded-full bg-body-mid" />
        )}
      </button>
      
      {label && (
        <span className="font-body-sm text-ink">{label}</span>
      )}
    </label>
  )
}
