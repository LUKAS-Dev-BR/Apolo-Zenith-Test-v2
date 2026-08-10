import { useState } from 'react'
import axios from 'axios'

interface SendMessageParams {
  message: string
  reasoningMode?: string
}

interface ChatResponse {
  response: string
  intent?: string
  media_request?: Record<string, unknown>
}

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sendMessage = async ({ message, reasoningMode = 'normal' }: SendMessageParams): Promise<ChatResponse | null> => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post<ChatResponse>('/api/chat/send', {
        message,
        reasoning_mode: reasoningMode
      })

      return response.data
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao enviar mensagem'
      setError(errorMessage)
      return null
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading,
    error
  }
}
