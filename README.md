# VoxAI - Chat IA Católica ✝️🤖

## Descrição do Projeto 📖
O **VoxAI** é um chatbot de inteligência artificial voltado para fornecer informações precisas e confiáveis sobre a doutrina católica.  
Ele tem como objetivo central combater a desinformação que circula sobre a Igreja Católica, consultando diretamente documentos oficiais como:

- 📜**Catecismo da Igreja Católica**
- ⚖️**Código de Direito Canônico**
- ✉️**Encíclicas papais**
- 📖**Bíblia Católica**
- 🏛️Outros documentos oficiais e relevantes da Igreja

O sistema lê PDFs de documentos importantes, processa seus trechos e utiliza embeddings para buscar respostas precisas às perguntas dos usuários. Todas as respostas são baseadas nos documentos originais, citando artigos, cânones ou versículos bíblicos quando aplicável.

---

## Estrutura do Projeto 📂

```
voxAI/
│
├── backend/          # Código da API FastAPI
│   └── app.py        # Expõe a função responder_com_documentos para o frontend
│
├── frontend/         # Frontend React com Vite
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── components/
│           ├── Chat.jsx
│           └── Message.jsx
│
├── data/
│   └── pdfs/ (Contém todos os pdfs para consulta de informação)
│
├── embeddings/
│   └── embeddings.pkl (gerado automaticamente)
│
├── src/
│   ├── chat.py
│   ├── config.py
│   ├── embeddings.py
│   ├── pdf_processor.py
│   └── vector_db.py
│
├── main.py
├── requirements.txt
└── .gitignore
```
---

## Configuração ⚙️

1. **Instalação das dependências**:

```bash
pip install -r requirements.txt
```

2. **Configuração da API Key do OpenAI**:

No arquivo src/config.py, coloque sua chave da OpenAI:
```python
OPENAI_API_KEY = "sua_api_key_aqui"
```

3. **PDFs** 📄
Coloque todos os PDFs oficiais da Igreja em `data/pdfs/`.

4. **Embeddings** 🧠
O arquivo `embeddings/embeddings.pkl` é gerado automaticamente pelo projeto na primeira execução e **não precisa ser enviado ao GitHub**.  
Ele contém os vetores de embeddings de todos os trechos dos PDFs.

## Como Funciona ⚡

### Extração de texto dos PDFs 📄
Cada PDF é lido e seu conteúdo é dividido em **chunks** de tamanho definido (`CHUNK_SIZE = 500 palavras`).

### Criação de embeddings 🧠
Cada chunk é transformado em um vetor numérico usando o modelo `text-embedding-ada-002` da OpenAI.  
Esses vetores permitem buscar trechos relevantes de acordo com a pergunta do usuário.

### Busca por relevância 🔍
Quando uma pergunta é feita, um embedding da pergunta é criado e comparado com os embeddings dos trechos usando **similaridade cosseno**.  
São selecionados os `TOP_K` trechos mais relevantes para formar o contexto.

### Geração da resposta 📝
O prompt enviado ao modelo ChatGPT inclui os trechos relevantes e instruções detalhadas para que a IA responda:

- Cite sempre o documento e o número do artigo/cânon ou versículo.
- Coloque trechos literais entre **aspas duplas**.
- Faça um resumo simples e compreensível.
- Nunca invente referências.

### Histórico de conversas 🗂️
O chat mantém o histórico das interações, permitindo respostas mais contextualizadas ao longo da conversa.

## Executando o Chat ▶️

### 1. Iniciando o Backend (Python)

No terminal, dentro da pasta do projeto `(chatVatican/)`:

```bash
python -m uvicorn backend.app:app --reload
```

- O backend ficará rodando em `http://127.0.0.1:8000`.
- Este serviço é responsável por receber suas perguntas e enviar respostas baseadas nos PDFs da Igreja.

### 2. Iniciando o Frontend (React)

No terminal, dentro da pasta `frontend/`:

```bash
npm install
npm run dev
```

- O frontend abrirá em algo como `http://127.0.0.1:5173` ou a porta indicada no terminal.
- Aqui você verá a interface do chat, com o histórico de mensagens e um campo para digitar perguntas.

### 3. Como usar

- Digite sua pergunta no campo de texto do chat e pressione **Enter** ou clique em **Enviar**.
- A resposta do VoxAI será exibida logo abaixo.
- Para encerrar, basta fechar a janela do navegador ou o terminal.

## Configurações Importantes ⚙️

No `src/config.py`:

```python
OPENAI_API_KEY = "sua_api_key"
PDF_PATH = "data/pdfs"          # Local dos PDFs
EMBEDDINGS_PATH = "embeddings/embeddings.pkl"
CHUNK_SIZE = 500                # Número de palavras por chunk
TOP_K = 3                       # Número de trechos relevantes usados por pergunta
```

## Observações ℹ️

- **Segurança** 🔒: PDFs e embeddings não são versionados no GitHub.

- **Precisão** ✅: As respostas são baseadas exclusivamente nos PDFs fornecidos.

- **Extensibilidade** ➕: É possível adicionar novos PDFs à pasta `data/pdfs` e o sistema atualizará os embeddings automaticamente na primeira execução.
