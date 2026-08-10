# Perguntas Frequentes - Apolo Zenith 1.9

## Geral

### O que é o Apolo Zenith 1.9?
O Apolo Zenith 1.9 é uma inteligência artificial multimodal unificada com capacidades de texto, imagem, vídeo, áudio e música. Ele inclui um LLM causal de 199B parâmetros e uma janela de contexto de 100 sexdecilhões de tokens.

### Quais são as principais funcionalidades?
- Chat conversacional avançado
- Geração de imagens
- Geração de vídeos
- Geração de áudio
- Geração de música
- Codificação agentica
- Modelagem 3D profissional
- 6 modos de raciocínio

## Instalação

### Quais são os requisitos mínimos?
- Python 3.8+
- Node.js 18+
- 16GB de RAM (recomendado)
- 50GB de espaço em disco

### Como instalar?
Execute o script de instalação:
```bash
./install.sh
```

Ou use Docker Compose:
```bash
docker-compose up
```

## Uso

### Como iniciar o sistema?
```bash
./start.sh
```

Ou manualmente:
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

### Onde acessar a interface?
- Frontend: http://localhost:3000
- API: http://localhost:8000

## Funcionalidades

### Como usar a codificação agentica?
Envie comandos como:
- "Leia o arquivo example.py"
- "Crie um script Python para calcular Fibonacci"
- "Execute o comando ls -la"

### Como usar a modelagem 3D?
Envie comandos como:
- "Crie um cubo na posição (0, 0, 0)"
- "Adicione uma luz puntual"
- "Exporte a cena para Blender"

### Como mudar o modo de raciocínio?
Selecione o modo desejado no menu lateral:
- Normal
- Médio
- Alto
- Muito Alto
- Ultra Alto
- Ultra Mega Alto

## Problemas Comuns

### O sistema não inicia
1. Verifique se todas as dependências estão instaladas
2. Verifique se as portas 8000 e 3000 estão livres
3. Consulte os logs de erro

### A geração de mídia é lenta
1. Verifique a memória disponível
2. Use um modo de raciocínio mais leve
3. Reduza a resolução/sampleduração

### Erros de autenticação
1. Verifique se a API key está correta
2. Gere uma nova key se necessário
3. Verifique o formato da key (az-...)

## Suporte

### Como reportar bugs?
Abra uma issue no repositório com:
- Descrição do problema
- Passos para reproduzir
- Logs de erro (se disponível)
- Versão do sistema

### Como solicitar funcionalidades?
Abra uma issue com a tag "enhancement" e descreva:
- A funcionalidade desejada
- Casos de uso
- Benefícios esperados
