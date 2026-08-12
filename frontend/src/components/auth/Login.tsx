import { useState } from 'react'
import { User } from '../../App'

interface LoginProps {
  onLogin: (user: User, token: string) => void
}

export default function Login({ onLogin }: LoginProps) {
  const [isRegister, setIsRegister] = useState(false)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const endpoint = isRegister ? '/api/auth/register' : '/api/auth/login'
      const body = isRegister
        ? { username, email, password }
        : { username, password }

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail || 'Erro ao processar solicitação')
        return
      }

      onLogin({ user_id: data.user_id, username: data.username }, data.access_token)
    } catch (e) {
      setError('Erro de conexão com o servidor')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-canvas flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="font-display-sm text-ink mb-2">Apolo Zenith</h1>
          <span className="font-caption-mono text-mute">1.9</span>
          <p className="font-body-md text-body mt-4">
            IA Multimodal Unificada
          </p>
        </div>

        <div className="card">
          <div className="flex border-b border-hairline mb-6">
            <button
              onClick={() => { setIsRegister(false); setError('') }}
              className={`flex-1 pb-3 font-body-sm transition-colors ${
                !isRegister ? 'text-ink border-b-2 border-ink' : 'text-body-mid hover:text-ink'
              }`}
            >
              Entrar
            </button>
            <button
              onClick={() => { setIsRegister(true); setError('') }}
              className={`flex-1 pb-3 font-body-sm transition-colors ${
                isRegister ? 'text-ink border-b-2 border-ink' : 'text-body-mid hover:text-ink'
              }`}
            >
              Cadastrar
            </button>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-900/30 border border-red-500 text-red-200 font-body-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="font-caption-mono text-mute block mb-2">Usuário</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field w-full"
                placeholder="Digite seu usuário"
                required
              />
            </div>

            {isRegister && (
              <div>
                <label className="font-caption-mono text-mute block mb-2">Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field w-full"
                  placeholder="Digite seu email"
                  required={isRegister}
                />
              </div>
            )}

            <div>
              <label className="font-caption-mono text-mute block mb-2">Senha</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field w-full"
                placeholder="Digite sua senha"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3"
            >
              {loading ? 'Processando...' : isRegister ? 'Criar Conta' : 'Entrar'}
            </button>
          </form>
        </div>

        <p className="text-center font-caption-mono-sm text-mute mt-6">
          Apolo Zenith 1.9 · Protegido com criptografia
        </p>
      </div>
    </div>
  )
}
