import React from 'react'
import { Eyebrow } from './Components'

interface FormGroupProps {
  label: string
  children: React.ReactNode
  description?: string
  error?: string
  className?: string
}

export function FormGroup({ label, children, description, error, className = '' }: FormGroupProps) {
  return (
    <div className={`space-y-2 ${className}`}>
      <Eyebrow>{label}</Eyebrow>
      
      {children}
      
      {description && !error && (
        <p className="font-body-sm text-mute">{description}</p>
      )}
      
      {error && (
        <p className="font-body-sm text-red-400">{error}</p>
      )}
    </div>
  )
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string
  options: { value: string; label: string }[]
  description?: string
  error?: string
}

export function Select({ label, options, description, error, className = '', ...props }: SelectProps) {
  return (
    <FormGroup label={label} description={description} error={error}>
      <select
        className={`input-field w-full ${error ? 'border-red-500' : ''} ${className}`}
        {...props}
      >
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </FormGroup>
  )
}

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string
  description?: string
  error?: string
}

export function TextareaInput({ label, description, error, className = '', ...props }: TextareaProps) {
  return (
    <FormGroup label={label} description={description} error={error}>
      <textarea
        className={`input-field w-full resize-none ${error ? 'border-red-500' : ''} ${className}`}
        {...props}
      />
    </FormGroup>
  )
}

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  description?: string
  error?: string
}

export function InputField({ label, description, error, className = '', ...props }: InputProps) {
  return (
    <FormGroup label={label} description={description} error={error}>
      <input
        className={`input-field w-full ${error ? 'border-red-500' : ''} ${className}`}
        {...props}
      />
    </FormGroup>
  )
}
