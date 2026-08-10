import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'outline' | 'outline-sm'
  children: React.ReactNode
}

export function Button({ variant = 'outline', className = '', children, ...props }: ButtonProps) {
  const baseStyles = 'font-button transition-all duration-200'
  
  const variantStyles = {
    primary: 'btn-primary',
    outline: 'btn-outline',
    'outline-sm': 'btn-outline-sm'
  }

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className = '', ...props }: InputProps) {
  return (
    <input
      className={`input-field w-full ${className}`}
      {...props}
    />
  )
}

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

export function Textarea({ className = '', ...props }: TextareaProps) {
  return (
    <textarea
      className={`input-field w-full resize-none ${className}`}
      {...props}
    />
  )
}

interface CardProps {
  children: React.ReactNode
  variant?: 'default' | 'soft'
  className?: string
}

export function Card({ children, variant = 'default', className = '' }: CardProps) {
  const variantStyles = {
    default: 'card',
    soft: 'card-soft'
  }

  return (
    <div className={`${variantStyles[variant]} ${className}`}>
      {children}
    </div>
  )
}

interface EyebrowProps {
  children: React.ReactNode
  className?: string
}

export function Eyebrow({ children, className = '' }: EyebrowProps) {
  return (
    <span className={`font-caption-mono text-ink ${className}`}>
      {children}
    </span>
  )
}

interface DividerProps {
  className?: string
}

export function Divider({ className = '' }: DividerProps) {
  return (
    <hr className={`border-hairline ${className}`} />
  )
}

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
}

export function IconButton({ className = '', children, ...props }: IconButtonProps) {
  return (
    <button
      className={`btn-outline-sm p-2 ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
