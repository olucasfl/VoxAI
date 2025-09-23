# VoxAI - Chat IA Católica

## Descrição do Projeto
O **VoxAI** é um chatbot de inteligência artificial voltado para fornecer informações precisas e confiáveis sobre a doutrina católica.  
Ele tem como objetivo central combater a desinformação que circula sobre a Igreja Católica, consultando diretamente documentos oficiais como:

- **Catecismo da Igreja Católica**
- **Código de Direito Canônico**
- **Encíclicas papais**
- **Bíblia Católica**
- Outros documentos oficiais e relevantes da Igreja

O sistema lê PDFs de documentos importantes, processa seus trechos e utiliza embeddings para buscar respostas precisas às perguntas dos usuários. Todas as respostas são baseadas nos documentos originais, citando artigos, cânones ou versículos bíblicos quando aplicável.

---

## Estrutura do Projeto

chatVatican/
│
├── data/ # 📂 Dados locais (não enviados ao GitHub)
│ └── pdfs/ # PDFs oficiais da Igreja (Catecismo, encíclicas, Código de Direito Canônico, Bíblia, etc.)
│
├── embeddings/ # 📂 Embeddings gerados a partir dos PDFs (não enviados ao GitHub)
│ └── embeddings.pkl # Arquivo que armazena os vetores de embeddings
│
├── src/ # 📂 Código fonte principal
│ ├── chat.py # Lógica principal do chat e integração com OpenAI
│ ├── embeddings.py # Funções para gerar, salvar e carregar embeddings
│ ├── pdf_processor.py # Funções para extrair texto dos PDFs e criar trechos/chunks
│ ├── vector_db.py # Busca de trechos relevantes usando embeddings
│ └── config.py # Configurações do projeto (caminhos, chaves e parâmetros)
│
├── main.py # Script de execução do chat no terminal
├── requirements.txt # Dependências do Python
└── .gitignore # Ignora pastas/pastas sensíveis como PDF e embeddings

---

## Configuração

1. **Instalação das dependências**:

```bash
pip install -r requirements.txt
```

2. **Configuração da API Key do OpenAI**:

No arquivo src/config.py, coloque sua chave da OpenAI:
```python
OPENAI_API_KEY = "sua_api_key_aqui"
```

3. **PDFs**:
Coloque todos os PDFs oficiais da Igreja em `data/pdfs/`.

4. **Embeddings**:
O arquivo `embeddings/embeddings.pkl` é gerado automaticamente pelo projeto na primeira execução e **não precisa ser enviado ao GitHub**.  
Ele contém os vetores de embeddings de todos os trechos dos PDFs.

## Como Funciona

### Extração de texto dos PDFs
Cada PDF é lido e seu conteúdo é dividido em **chunks** de tamanho definido (`CHUNK_SIZE = 500 palavras`).

### Criação de embeddings
Cada chunk é transformado em um vetor numérico usando o modelo `text-embedding-ada-002` da OpenAI.  
Esses vetores permitem buscar trechos relevantes de acordo com a pergunta do usuário.

### Busca por relevância
Quando uma pergunta é feita, um embedding da pergunta é criado e comparado com os embeddings dos trechos usando **similaridade cosseno**.  
São selecionados os `TOP_K` trechos mais relevantes para formar o contexto.

### Geração da resposta
O prompt enviado ao modelo ChatGPT inclui os trechos relevantes e instruções detalhadas para que a IA responda:

- Cite sempre o documento e o número do artigo/cânon ou versículo.
- Coloque trechos literais entre **aspas duplas**.
- Faça um resumo simples e compreensível.
- Nunca invente referências.

### Histórico de conversas
O chat mantém o histórico das interações, permitindo respostas mais contextualizadas ao longo da conversa.

## Executando o Chat

Para iniciar o chat no terminal, use:

```python
python main.py
```

- Digite sua pergunta e pressione Enter.
- Para encerrar, digite: `sair`.

Exemplo de interação:

```vbnet
Pergunta: O que o Catecismo diz sobre pecado mortal?
Vox: Vamos lá, de acordo com o Catecismo da Igreja Católica, 1857 diz que: "Para que um pecado seja mortal, é necessário que haja matéria grave, pleno conhecimento e deliberação."
Resumo: Um pecado é considerado mortal quando envolve algo grave, é feito com plena consciência e escolha voluntária.
```

## Configurações Importantes

No `src/config.py`:

```python
OPENAI_API_KEY = "sua_api_key"
PDF_PATH = "data/pdfs"          # Local dos PDFs
EMBEDDINGS_PATH = "embeddings/embeddings.pkl"
CHUNK_SIZE = 500                # Número de palavras por chunk
TOP_K = 3                       # Número de trechos relevantes usados por pergunta
```

## Observações

- **Segurança**: PDFs e embeddings não são versionados no GitHub.

- **Precisão**: As respostas são baseadas exclusivamente nos PDFs fornecidos.

- **Extensibilidade**: É possível adicionar novos PDFs à pasta `data/pdfs` e o sistema atualizará os embeddings automaticamente na primeira execução.
