import React from 'react'
import ReactMarkdown from 'react-markdown'
import { CopyIcon, RefreshIcon } from '../ui/Icons'

interface MessageProps {
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: Date
  }
  onCopy?: () => void
  onRegenerate?: () => void
}

export default function Message({ message, onCopy, onRegenerate }: MessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[85%] ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Avatar */}
        <div className={`flex items-center gap-2 mb-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
          <div className={`w-6 h-6 rounded-full flex items-center justify-center ${
            isUser ? 'bg-canvas-mid' : 'bg-accent-dusk'
          }`}>
            <span className="font-caption-mono-sm text-ink">
              {isUser ? 'U' : 'AZ'}
            </span>
          </div>
          <span className="font-caption-mono-sm text-mute">
            {isUser ? 'Você' : 'Apolo Zenith'}
          </span>
          <span className="font-caption-mono-sm text-mute">
            {message.timestamp.toLocaleTimeString('pt-BR', { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </span>
        </div>

        {/* Message Content */}
        <div className={`rounded-xl p-4 ${
          isUser 
            ? 'bg-canvas-soft border border-hairline' 
            : 'bg-canvas-card border border-hairline'
        }`}>
          {isUser ? (
            <p className="font-body-md text-ink whitespace-pre-wrap">
              {message.content}
            </p>
          ) : (
            <div className="font-body-md text-body">
              <ReactMarkdown
                components={{
                  code({ className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '')
                    const isInline = !match && !className
                    
                    if (isInline) {
                      return (
                        <code 
                          className="bg-canvas-mid px-1.5 py-0.5 rounded text-accent-sunset-soft text-sm"
                          {...props}
                        >
                          {children}
                        </code>
                      )
                    }
                    
                    return (
                      <div className="my-2">
                        {match && (
                          <div className="bg-canvas-mid px-4 py-2 text-xs text-mute border-b border-hairline rounded-t-lg">
                            {match[1]}
                          </div>
                        )}
                        <code 
                          className={`block bg-canvas-mid p-4 overflow-x-auto ${match ? 'rounded-b-lg' : 'rounded-lg'}`}
                          {...props}
                        >
                          {children}
                        </code>
                      </div>
                    )
                  },
                  p({ children }) {
                    return <p className="mb-2 last:mb-0">{children}</p>
                  },
                  ul({ children }) {
                    return <ul className="list-disc list-inside mb-2">{children}</ul>
                  },
                  ol({ children }) {
                    return <ol className="list-decimal list-inside mb-2">{children}</ol>
                  },
                  li({ children }) {
                    return <li className="mb-1">{children}</li>
                  },
                  h1({ children }) {
                    return <h1 className="font-display-sm text-ink mb-2">{children}</h1>
                  },
                  h2({ children }) {
                    return <h2 className="font-display-xs text-ink mb-2">{children}</h2>
                  },
                  h3({ children }) {
                    return <h3 className="font-body-lg text-ink font-medium mb-2">{children}</h3>
                  },
                  blockquote({ children }) {
                    return (
                      <blockquote className="border-l-2 border-accent-dusk pl-4 my-2 text-body-mid">
                        {children}
                      </blockquote>
                    )
                  },
                  a({ href, children }) {
                    return (
                      <a 
                        href={href} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-accent-breeze hover:underline"
                      >
                        {children}
                      </a>
                    )
                  }
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Actions */}
        {!isUser && (
          <div className="flex items-center gap-3 mt-2">
            <button 
              onClick={onCopy}
              className="flex items-center gap-1.5 font-caption-mono-sm text-mute hover:text-ink transition-colors"
            >
              <CopyIcon size={14} />
              <span>Copiar</span>
            </button>
            {onRegenerate && (
              <>
                <span className="text-canvas-mid">·</span>
                <button 
                  onClick={onRegenerate}
                  className="flex items-center gap-1.5 font-caption-mono-sm text-mute hover:text-ink transition-colors"
                >
                  <RefreshIcon size={14} />
                  <span>Regenerar</span>
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
