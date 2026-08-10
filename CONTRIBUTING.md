# Contribuindo para o Apolo Zenith 1.9

Obrigado por seu interesse em contribuir com o Apolo Zenith 1.9!

## Diretrizes

### Código
- Siga o estilo de código existente
- Adicione comentários quando necessário
- Escreva testes para novas funcionalidades
- Execute lint e typecheck antes de enviar

### Commits
- Use mensagens de commit claras e descritivas
- Siga o formato: `tipo(escopo): descrição`
- Exemplos:
  - `feat(llm): adicionar suporte a novos tokens`
  - `fix(multimodal): corrigir bug na geração de imagem`
  - `docs(readme): atualizar documentação`

### Pull Requests
- Crie um branch para sua funcionalidade
- Descreva as mudanças no PR
- Inclua testes quando aplicável
- Solicite revisão de pelo menos um mantenedor

## Estrutura do Projeto

### Backend
- `backend/app/api/routes/` - Rotas da API
- `backend/app/core/llm/` - Core do LLM
- `backend/app/core/multimodal/` - Motores multimodais
- `backend/app/core/agents/` - Agentes
- `backend/app/core/infrastructure/` - Infraestrutura

### Frontend
- `frontend/src/components/` - Componentes React
- `frontend/src/hooks/` - Hooks personalizados
- `frontend/src/store/` - Estado global
- `frontend/src/utils/` - Utilitários

## Desenvolvimento

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Testes

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run lint
npm run build
```

## Perguntas?

Se tiver dúvidas, abra uma issue no repositório.
