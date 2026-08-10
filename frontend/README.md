# Apolo Zenith 1.9 - Frontend

## Visão Geral

O frontend do Apolo Zenith 1.9 é construído com React e TypeScript, seguindo o design system do xAI.

## Estrutura

```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── Chat.tsx
│   │   │   └── Message.tsx
│   │   └── ui/
│   │       ├── Components.tsx
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       ├── Loading.tsx
│   │       ├── Toast.tsx
│   │       ├── Modal.tsx
│   │       ├── Tooltip.tsx
│   │       ├── Badge.tsx
│   │       ├── Cards.tsx
│   │       ├── Forms.tsx
│   │       ├── List.tsx
│   │       ├── Table.tsx
│   │       ├── Tabs.tsx
│   │       ├── Accordion.tsx
│   │       ├── Popover.tsx
│   │       ├── Dropdown.tsx
│   │       ├── Skeleton.tsx
│   │       ├── Avatar.tsx
│   │       ├── Progress.tsx
│   │       ├── Switch.tsx
│   │       ├── Alert.tsx
│   │       ├── Breadcrumb.tsx
│   │       └── Pagination.tsx
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useApiKeys.ts
│   │   └── useMedia.ts
│   ├── store/
│   │   └── index.ts
│   ├── utils/
│   │   └── index.ts
│   ├── styles/
│   │   └── globals.css
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── postcss.config.js
```

## Design System

O frontend segue o design system do xAI com as seguintes características:

### Cores

- **Canvas**: `#0a0a0a` - Fundo principal
- **Canvas Soft**: `#1a1c20` - Superfícies secundárias
- **Canvas Card**: `#191919` - Cards
- **Ink**: `#ffffff` - Texto principal
- **Body**: `#dadbdf` - Texto secundário
- **Hairline**: `#212327` - Bordas

### Tipografia

- **Display XL**: 96px, tracking -2.4px
- **Display LG**: 72px, tracking -1.8px
- **Display MD**: 48px, tracking -1.2px
- **Display SM**: 32px, tracking -0.6px
- **Body LG**: 18px
- **Body MD**: 16px
- **Body SM**: 14px
- **Caption Mono**: 14px, tracking 1.4px, uppercase

### Componentes

- **Botões**: Pill shape (border-radius: 9999px)
- **Cards**: Border-radius 8px, borda hairline
- **Inputs**: Background canvas-soft, borda hairline

## Instalação

```bash
cd frontend
npm install
npm run dev
```

## Uso

O frontend se comunica com o backend via API REST:

- `POST /api/chat/send` - Enviar mensagem
- `GET /api/auth/keys` - Listar chaves de API
- `POST /api/auth/keys` - Criar chave de API
- `POST /api/media/generate` - Gerar mídia
- `GET /api/media/status/:job_id` - Verificar status
- `GET /api/media/progress/:job_id` - Verificar progresso
