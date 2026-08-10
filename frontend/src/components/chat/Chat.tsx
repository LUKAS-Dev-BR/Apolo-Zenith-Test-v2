import React, { useState, useRef, useEffect } from 'react'
import { Button, Card, Eyebrow } from '../ui/Components'
import { ArrowUpIcon, CopyIcon, RefreshIcon } from '../ui/Icons'
import Message from './Message'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault()
    
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input.trim(),
          reasoning_mode: 'normal'
        })
      })

      const data = await response.json()

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error)
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content)
  }

  return (
    <div className="flex flex-col h-full bg-canvas">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map(message => (
              <Message 
                key={message.id} 
                message={message}
                onCopy={() => copyMessage(message.content)}
              />
            ))}
            
            {isLoading && (
              <div className="flex items-center gap-2 text-body-mid pl-10">
                <div className="w-2 h-2 bg-body-mid rounded-full animate-pulse-subtle" />
                <div className="w-2 h-2 bg-body-mid rounded-full animate-pulse-subtle" style={{ animationDelay: '0.2s' }} />
                <div className="w-2 h-2 bg-body-mid rounded-full animate-pulse-subtle" style={{ animationDelay: '0.4s' }} />
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-hairline p-4 md:p-6 bg-canvas">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div className="relative bg-canvas-soft border border-hairline rounded-xl overflow-hidden focus-within:border-body-mid transition-colors">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Enviar mensagem para Apolo Zenith..."
              className="w-full px-4 py-3 pr-12 bg-transparent text-ink placeholder-mute font-body-md resize-none focus:outline-none min-h-[48px] max-h-[200px]"
              rows={1}
              disabled={isLoading}
            />
            
            <div className="absolute right-2 bottom-2">
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className={`p-2 rounded-lg transition-all duration-200 ${
                  input.trim() && !isLoading
                    ? 'bg-ink text-on-primary hover:bg-ink-hover'
                    : 'bg-canvas-mid text-mute cursor-not-allowed'
                }`}
              >
                <ArrowUpIcon size={18} />
              </button>
            </div>
          </div>
          
          <p className="mt-2 text-center font-caption-mono-sm text-mute">
            Apolo Zenith 1.9 · Enter para enviar · Shift+Enter para nova linha
          </p>
        </form>
      </div>
    </div>
  )
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full px-4">
      <div className="text-center max-w-2xl">
        <h1 className="font-display-md text-ink mb-4">
          Apolo Zenith 1.9
        </h1>
        <Eyebrow className="mb-6 block">
          IA Multimodal Unificada
        </Eyebrow>
        <p className="font-body-lg text-body mb-8">
          Uma inteligência artificial de última geração com capacidades de texto, imagem, vídeo, áudio e música.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <Eyebrow className="mb-2 block">Texto</Eyebrow>
            <p className="font-body-sm text-body">
              LLM causal de 199B parâmetros com janela de contexto de 100 sexdecilhões de tokens.
            </p>
          </Card>
          
          <Card>
            <Eyebrow className="mb-2 block">Imagem</Eyebrow>
            <p className="font-body-sm text-body">
              Geração de imagens via difusão com U-Net 2D e Cross-Attention.
            </p>
          </Card>
          
          <Card>
            <Eyebrow className="mb-2 block">Vídeo</Eyebrow>
            <p className="font-body-sm text-body">
              Geração de vídeos com U-Net 3D e atenção temporal.
            </p>
          </Card>
          
          <Card>
            <Eyebrow className="mb-2 block">Áudio & Música</Eyebrow>
            <p className="font-body-sm text-body">
              Pipeline DSP com difusão de espectrogramas e vocoder neural.
            </p>
          </Card>
        </div>
        
        <div className="mt-8">
          <Card variant="soft">
            <Eyebrow className="mb-2 block">Agentes</Eyebrow>
            <p className="font-body-sm text-body">
              Codificação agentica com 6 modos de raciocínio e capacidade de modelagem 3D profissional.
            </p>
          </Card>
        </div>
      </div>
    </div>
  )
}
