import { useState, useCallback } from 'react'
import axios from 'axios'

interface MediaJob {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  media_type: string
  prompt: string
  progress: number
  result_path?: string
  error?: string
}

export function useMedia() {
  const [jobs, setJobs] = useState<MediaJob[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const generateMedia = async (mediaType: string, prompt: string, parameters?: Record<string, unknown>): Promise<string | null> => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post<{ job_id: string }>('/api/media/generate', {
        media_type: mediaType,
        prompt,
        parameters
      })

      const newJob: MediaJob = {
        job_id: response.data.job_id,
        status: 'pending',
        media_type: mediaType,
        prompt,
        progress: 0
      }

      setJobs(prev => [...prev, newJob])
      return response.data.job_id
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao gerar mídia'
      setError(errorMessage)
      return null
    } finally {
      setIsLoading(false)
    }
  }

  const checkProgress = useCallback(async (jobId: string) => {
    try {
      const response = await axios.get<{ progress: number }>(`/api/media/progress/${jobId}`)
      
      setJobs(prev => prev.map(job => 
        job.job_id === jobId 
          ? { ...job, progress: response.data.progress }
          : job
      ))
      
      return response.data.progress
    } catch (err) {
      console.error('Erro ao verificar progresso:', err)
      return null
    }
  }, [])

  const checkStatus = useCallback(async (jobId: string) => {
    try {
      const response = await axios.get<MediaJob>(`/api/media/status/${jobId}`)
      
      setJobs(prev => prev.map(job => 
        job.job_id === jobId 
          ? { ...job, ...response.data }
          : job
      ))
      
      return response.data
    } catch (err) {
      console.error('Erro ao verificar status:', err)
      return null
    }
  }, [])

  const pollProgress = useCallback((jobId: string, onComplete?: (result: MediaJob) => void) => {
    const interval = setInterval(async () => {
      const status = await checkStatus(jobId)
      
      if (status?.status === 'completed' || status?.status === 'failed') {
        clearInterval(interval)
        if (onComplete) {
          onComplete(status)
        }
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [checkStatus])

  return {
    jobs,
    isLoading,
    error,
    generateMedia,
    checkProgress,
    checkStatus,
    pollProgress
  }
}
