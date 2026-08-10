import React, { useEffect } from 'react'
import { IconButton } from './Components'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  children: React.ReactNode
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/70"
        onClick={onClose}
      />
      
      {/* Modal Content */}
      <div className="relative card max-w-md w-full mx-4 animate-fade-in">
        {/* Header */}
        {title && (
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display-xs text-ink">{title}</h2>
            <IconButton onClick={onClose}>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 6L6 18M6 6l12 12" />
              </svg>
            </IconButton>
          </div>
        )}
        
        {/* Body */}
        <div className="font-body-md text-body">
          {children}
        </div>
      </div>
    </div>
  )
}

interface ConfirmModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title: string
  message: string
  confirmText?: string
  cancelText?: string
}

export function ConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = 'Confirmar',
  cancelText = 'Cancelar'
}: ConfirmModalProps) {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title}>
      <p className="mb-6">{message}</p>
      
      <div className="flex justify-end gap-3">
        <button 
          onClick={onClose}
          className="btn-outline"
        >
          {cancelText}
        </button>
        <button 
          onClick={() => {
            onConfirm()
            onClose()
          }}
          className="btn-primary"
        >
          {confirmText}
        </button>
      </div>
    </Modal>
  )
}
