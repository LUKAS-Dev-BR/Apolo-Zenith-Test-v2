import { useState, useEffect } from 'react'
import axios from 'axios'

interface ApiKey {
  key_prefix: string
  name: string
  created_at: number
}

export function useApiKeys() {
  const [keys, setKeys] = useState<ApiKey[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchKeys = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.get<ApiKey[]>('/api/auth/keys')
      setKeys(response.data)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao buscar chaves'
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const createKey = async (name: string): Promise<string | null> => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post<{ key: string }>('/api/auth/keys', { name })
      await fetchKeys()
      return response.data.key
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao criar chave'
      setError(errorMessage)
      return null
    } finally {
      setIsLoading(false)
    }
  }

  const deleteKey = async (keyHash: string): Promise<boolean> => {
    setIsLoading(true)
    setError(null)

    try {
      await axios.delete(`/api/auth/keys/${keyHash}`)
      await fetchKeys()
      return true
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao deletar chave'
      setError(errorMessage)
      return false
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchKeys()
  }, [])

  return {
    keys,
    isLoading,
    error,
    fetchKeys,
    createKey,
    deleteKey
  }
}
