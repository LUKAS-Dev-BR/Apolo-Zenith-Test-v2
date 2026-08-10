# Apolo Zenith 1.9

## IA Multimodal Unificada

Uma inteligência artificial de última geração com capacidades de texto, imagem, vídeo, áudio e música.

## Características

### Core de Linguagem (LLM Causal de 199B)
- Transformer autoregressivo causal
- Janela de contexto de 100 sexdecilhões de tokens
- Tokenização via SentencePiece
- Saída estruturada JSON para geração de mídia

### Motores Multimodais
- **Text-to-Image**: U-Net 2D com Cross-Attention
- **Text-to-Video**: U-Net 3D com Atenção Temporal
- **Text-to-Audio**: Difusão de Espectrogramas + Vocoder
- **Text-to-Música**: Pipeline DSP + U-Net de Denoising

### Agentes
- **Codificação Agentica**:
  - Dev Sênior Front-end
  - Dev Sênior Back-end
  - 9.000+ linguagens de programação
  - Designer Front-end profissional
- **Modelagem 3D Profissional**:
  - Criação de malhas 3D
  - Materiais e texturas
  - Iluminação
  - Exportação para Blender

### Modos de Raciocínio
1. **Normal**: Profundidade 1, 1024 tokens
2. **Médio**: Profundidade 2, 2048 tokens
3. **Alto**: Profundidade 4, 4096 tokens
4. **Muito Alto**: Profundidade 8, 8192 tokens
5. **Ultra Alto**: Profundidade 16, 16384 tokens
6. **Ultra Mega Alto**: Profundidade 32, 32768 tokens

## Arquitetura

### Backend
- Python + FastAPI
- PyTorch para modelos de IA
- SQLite para fila de jobs
- Armazenamento local para mídia

### Frontend
- React + TypeScript
- Tailwind CSS
- Design System xAI
- Interface responsiva

## Instalação

### Opção 1: Instalação Manual

```bash
# Executar script de instalação
./install.sh

# Iniciar o projeto
./start.sh
```

### Opção 2: Docker Compose

```bash
docker-compose up
```

## Uso

### Backend API

- `GET /` - Informações da API
- `GET /health` - Status do sistema
- `GET /api/capabilities` - Capacidades do sistema
- `POST /api/chat/send` - Enviar mensagem
- `POST /api/media/generate` - Gerar mídia
- `GET /api/media/status/:job_id` - Verificar status
- `GET /api/media/progress/:job_id` - Verificar progresso
- `POST /api/agents/code/execute` - Executar comando de código
- `POST /api/agents/modeling/execute` - Executar comando de modelagem

### Frontend

Acesse http://localhost:3000 para usar a interface de chat.

## Estrutura do Projeto

```
Apolo Zenith 1.9/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   │   ├── llm/
│   │   │   ├── multimodal/
│   │   │   ├── agents/
│   │   │   ├── infrastructure/
│   │   │   ├── safety/
│   │   │   └── training/
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── store/
│   │   └── utils/
│   └── package.json
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Licença

Proprietário - Apolo Zenith 1.9
