Apolo Zenith 1.9 (IA Multimodal Unificada do Zero)
Crie a base de código completa, estruturada, modular e executável para um ecossistema de inteligência artificial de última geração chamado Apolo Zenith 1.9. O objetivo absoluto deste projeto é integrar um motor multimodal unificado (Texto, Imagem, Vídeo, Áudio e Música) operando de forma síncrona no espírito de plataformas como ChatGPT, DALL-E, Sora, Suno e ElevenLabs.

Restrição Arquitetural Estrita: Todos os motores generativos de mídia e o modelo de linguagem devem ser construídos inteiramente do zero, utilizando única e exclusivamente bibliotecas de tensores puros (PyTorch ou TensorFlow). É terminantemente proibido o uso da biblioteca Hugging Face (diffusers, transformers), de pesos pré-treinados externos ou de qualquer outra abstração de alto nível. Toda a matemática vetorial, matrizes de atenção e loops de difusão devem ser codificados explicitamente.

Parte 1 — O Core de Linguagem (LLM Causal de 199B)
Construir a arquitetura completa de um modelo Transformer autoregressivo (causal) em PyTorch, dimensionado para a escala massiva de 199 Bilhões de parâmetros ($199 \times 10^9$). O motor deve ser programado refletindo rigorosamente as quatro etapas mecânicas de processamento estatístico de grandes modelos de linguagem:

1.1 Pilares de Funcionamento Mecânico e Ciclo de Treinamento no Celular
Tokenização e Embeddings: Implementar a fragmentação de strings brutas em unidades discretas (tokens) via SentencePiece treinado localmente. Cada ID de token deve ser mapeado para um espaço vetorial contínuo de alta dimensão (embeddings posicionais e semânticos), convertendo linguagem humana em coordenadas matemáticas puras.
Análise de Contexto Global (Arquitetura Transformer): Implementar o mecanismo de Self-Attention (Atenção Causal com Máscara Inferior). O modelo não deve ler palavras isoladamente, mas sim computar simultaneamente o peso e a correlação de todos os tokens dentro da janela de contexto através de matrizes de projeção de Query ($Q$), Key ($K$) e Value ($V$).
Pré-treinamento Estatístico e Aprendizado Local no Celular: O modelo não depende de arquivos externos pré-prontos ou .md; em vez disso, o script de treinamento realiza o pré-treinamento estatístico base (Next-Token Prediction) processando corpora de textos armazenados localmente na memória do celular, calculando a probabilidade do próximo token de forma iterativa por lotes de tensores otimizados para arquiteturas móveis.
Alinhamento por Instrução (SFT & Formato Chat): Aplicar uma camada de Supervised Fine-Tuning (SFT) estruturada em turnos de diálogo (usuário / assistente), treinando o modelo localmente para assumir uma postura conversacional prestativa e emitir saídas estruturadas.
1.2 Configurações e Hiperparâmetros do LLM
Janela de Contexto: Fixada em uma janela flexível de até 100.096 tokens simultâneos.
Saída Estruturada de Mídia (JSON): Quando o LLM interceptar uma intenção de geração de mídia no prompt do usuário, ele deve cessar a geração de texto comum e responder obrigatoriamente com um esquema JSON estrito para acionar os motores da Parte 2:



JSON

{
 "intent": "generate_media",
 "media_type": "image | video | audio | music",
 "prompt": "...",
 "parameters": {"duration_seconds": 30, "aspect_ratio": "16:9", "bpm": 120}
}

Otimização: Loops de treino construídos com precisão mista (Mixed Precision / AMP) e acúmulo de gradiente (Gradient Accumulation), mitigando overfitting via Dropout e Weight Decay executados no ambiente móvel.
Parte 2 — Motores Multimodais do Zero (Sem Hugging Face)
Toda a geração visual e acústica deve ser codificada bloco a bloco através de matrizes de tensores puros em PyTorch.

2.1 A Base Matemática: Processo de Difusão Manual (DDPM)
Criar uma classe matemática isolada para gerenciar os schedules de ruído estocástico:

Processo Forward: Injeção linear ou em cosseno de ruído gaussiano programático sobre os tensores originais ao longo de $T=1000$ passos baseados na equação:
$$q(x_t \vert x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t}x_0, (1 - \bar{\alpha}_t)\mathbf{I})$$
Processo Backward: O loop reverso de inferência que recebe um tensor puramente caótico (estática) e, a cada passo decrementado, subtrai a fração exata de ruído prevista pelas redes neurais.
2.2 Motor Text-to-Image
Codificador de Texto Embutido: Extrator matemático de embeddings textuais baseado em um mini-Transformer CLIP construído na unha.
U-Net 2D Condicional: Blocos sequenciais de Downsampling, Bottleneck e Upsampling utilizando convoluções bidimensionais.
Mecanismo de Cross-Attention: Injetado explicitamente nos blocos da U-Net para cruzar os mapas de recursos da imagem ruidosa com os vetores do prompt de texto enviado pelo LLM.
2.3 Motor Text-to-Video (Extensão Temporal)
U-Net 3D Condicional: Evolução do motor convolucional para aceitar tensores de 5 dimensões: $[Batch, Channels, Frames, Height, Width]$.
Camadas de Atenção Temporal (Temporal Attention Blocks): Módulos de atenção aplicados especificamente e exclusivamente no eixo bidimensional do Tempo ($T$), forçando a coerência geométrica entre frames subsequentes e eliminando artefatos de oscilação caótica de pixels (flickering).
2.4 Motor Text-to-Audio e Geração de Músicas do Zero
O ecossistema acústico e musical deve processar o som através da física das frequências senoidais, tratando áudio como matrizes visuais de energia:

Pipeline DSP (Processamento Digital de Sinais): Criar rotinas puras baseadas na Transformada de Fourier de Curto Termo (torch.stft). O sistema deve ler arquivos .wav, fatiá-los em janelas de tempo e mapear as energias harmônicas na Escala de Mel (escala logarítmica que mimetiza a percepção auditiva humana). A saída deve ser um Espectrograma de Mel, isto é, uma "imagem" onde o eixo X representa o tempo, o eixo Y representa a frequência (graves ao agudos) e o valor do pixel representa a amplitude (volume).
U-Net de Denoising de Espectrogramas: Uma rede U-Net 2D especializada em processar as matrizes de Mel. A rede deve receber uma entrada de ruído estático puro (chiado) e, através de camadas de Cross-Attention alimentadas pela letra da música e estilo instrumental informados pelo LLM, remover o chiado pixel por pixel até desenhar as linhas de frequência harmônicas perfeitas da música.
Vocoder Neural (Sintetizador de Onda): Como os espectrogramas de Mel omitem a informação de fase da onda sonora, deve ser implementada uma rede baseada em Convoluções 1D Transpostas e blocos de ressonância dilatados (estilo HiFi-GAN/MelGAN). Esta rede deve ler o espectrograma limpo gerado pela difusão e reconstruir analiticamente a forma de onda contínua no tempo, convertendo os tensores de volta para um sinal físico de áudio estereofônico salvo em .wav.
Parte 3 — Infraestrutura, Stack e Arquivos Proprietários
3.1 Tabela de Stack Tecnológico
Camada

Stack Nativo

Restrição Técnica

LLM Causal (199B)

Python + PyTorch

Atenção causal, tokenização local e decodificação autoregressiva.

Motores de Mídia

Python + PyTorch / TensorFlow

Difusão de imagens, vídeos, áudios e músicas escritos sem Diffusers.

Backend / API

Python (FastAPI)

Orquestrador de endpoints e chamadas assíncronas.

Fila de Execução

Arquivo Binário Indexado / SQLite

Engenharia local em disco. Proibido Redis, SQS ou RabbitMQ.

Frontend

TypeScript + React (Vite)

Interface responsiva de Chat + Galeria Multimodal.

Storage de Mídia

Sistema de Arquivos Nativo (FS)

Armazenamento físico estruturado em partições locais de disco.

3.2 Engenharia de Infraestrutura Interna
Gerenciador de Fila Persistente: Módulo em Python que intercepta as requisições de geração do FastAPI, grava o estado do Job em um banco SQLite ou arquivo em disco, e despacha de forma ordenada para os motores de difusão, protegendo o pipeline contra desligamentos inesperados do servidor.
Módulo KV Store Local: Armazenamento em disco do tipo chave-valor para que o Frontend realize consultas contínuas (polling) e exiba o progresso exato da remoção do ruído (de 0% a 100%) em tempo real para o usuário.
Parte 4 — Fluxo Operacional, Segurança e Deploy
4.1 Ciclo de Vida de uma Requisição Multimodal
O usuário submete um comando no Frontend React (ex: "Gere um sintetizador cyberpunk dos anos 80 em 140 BPM").
O servidor de borda repassa a string para o Backend focado na inferência do LLM de 199B.
O LLM decodifica o texto via matrizes de atenção, reconhece a intenção musical e cospe o JSON parametrizado.
O Job de áudio é indexado na fila persistente local.
O motor de áudio assume, gera a matriz de estática pura, executa as 1000 passagens da U-Net limpando as frequências guiado pelo texto, e entrega o Espectrograma de Mel perfeito.
O Vocoder processa esse espectrograma, sintetiza as fases da onda e gera o arquivo .wav na partição do disco local.
O Frontend recupera o arquivo final via polling e renderiza o player de áudio na tela.
4.2 Camada de Moderação e Salvaguardas Críticas
Filtro Simétrico de Entrada: Algoritmo de correspondência matricial de tokens para bloquear instantaneamente prompts associados a violências explícitas, abusos de qualquer natureza, deepfakes não autorizados ou exploração prejudicial.
Filtro Analítico de Saída: Classificadores baseados em redes neurais convolucionais leves aplicadas diretamente nos tensores gerados (imagens, frames de vídeo e formas de onda) para interceptar, deletar do disco e impedir o envio de qualquer saída anômala ou que infrinja os termos de segurança do sistema.
Snapshot Automático: Scripts em Python para backup incremental agendado de todas as mídias e checkpoints gerados localmente.

detalhes importantes!

vc pode usar o ambiente virtual venv
a Apolo Zenith 1.9 deve ter funcionalidades de codificação agentica então essa funcionalidade de codificação agentica da Apolo Zenith 1.9 deve permitir que ela execute comando reais e criar arquivo, editar arquivos, ler arquivos, etc.
a Apolo Zenith 1.9 deve ser treinada em português brasileiro
e quando vc terminar a criação da Apolo Zenith 1.9 treine toda a Apolo Zenith 1.9 primeiro vc deve começar pelo pré-treino + SFT e depois que terminar o pré-treino + SFT vc deve começar o dataset/treino do LLM e depois que termina e Agora adicione mais de 100.000.000 ferramentas de codificação agentica para a Apolo Zenith 1.9 e eu quero que a Apolo Zenith 1.9 tenha a capacidade de modelagem de modelador 3D profissional sabe porque isso de modelagem 3D profissional porque eu tô pensando em criar uma cli para a Apolo Zenith 1.9 aí essa CLI é de codificação agentica igual ao Claude Code igual ao Codex aí vai ter a funcionalidade de MCP aí se o usuário conectar o MCP do blender a CLI a Apolo Zenith 1.9 já vai estar preparada sabe por quê porque ela vai ter a capacidade de modelagem 3D que o modelador 3D profissional e adicione 6 modos de raciocínio para a Apolo Zenith 1.9 primeiro modo de raciocínio Normal segundo modo de raciocínio médio terceiro modo de raciocínio alto quarto modo de raciocínio Muito Alto quinto modo de raciocínio Ultra Alto sexto modo de raciocínio Ultra Mega Alto e quando aumentado o modo de raciocínio da Apolo Zenith 1.9 melhor o resultado da codificação agentica da Apolo Zenith 1.9 e eu quero que vc adicione 4 capacidades de codificação agentica para a e eu quero que a 1 capacidade de codificação agentica da seja a capacidade de dev sênior front-end e a 2 capacidade de dev sênior Back-End e a 3 capacidade de programar nas 9.000 linguagens de programação e a 4 capacidade de designer front-end profissional e faça o design do chat com a Apolo Zenith 1.9 igual ao design do Claude.ai e igual ao design do chatgpt.com e eu quero que a Apolo Zenith 1.9 tenha uma API key no mesmo formato da API key do ChatGPT e do Claude
