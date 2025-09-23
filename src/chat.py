import os
import re
from openai import OpenAI
from .vector_db import buscar_trechos
from .config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Histórico global
historico = []

def formatar_nome_documento(nome_pdf):
    nome = os.path.splitext(nome_pdf)[0]
    nome = nome.replace("-", " ").replace("_", " ")
    return nome.title()

def extrair_artigo(texto):
    """
    Extrai o número do artigo/cânon no início do texto.
    Ex.: '1857. Para que um pecado seja mortal...'
    """
    match = re.match(r"^\s*(\d{1,4})\.", texto.strip())
    if match:
        return match.group(1)
    return None

def responder_com_documentos(pergunta, max_palavras=200):
    global historico

    # Limita a pergunta para evitar excesso de tokens
    palavras = pergunta.split()
    if len(palavras) > max_palavras:
        pergunta = " ".join(palavras[:max_palavras])
        print(f"A pergunta foi truncada para {max_palavras} palavras para economizar tokens.")

    # Busca trechos relevantes
    trechos_relevantes = buscar_trechos(pergunta)

    # Monta contexto com nome do documento e artigo/versículo
    contexto = ""
    for t in trechos_relevantes:
        doc_nome = formatar_nome_documento(t['documento'])
        artigo = extrair_artigo(t['texto'])
        if artigo:
            contexto += f"Trecho ({doc_nome}, {artigo}): {t['texto']}\n\n"
        else:
            contexto += f"Trecho ({doc_nome}): {t['texto']}\n\n"

    # Prompt detalhado
    prompt = f"""
Você se chama Vox e é um especialista em doutrina católica e documentos oficiais da Igreja.
Seu objetivo é fornecer respostas precisas, completas e corretas, sempre baseado em documentos oficiais (Catecismo, Código de Direito Canônico, encíclicas, Bíblia Católica, etc.).

IMPORTANTE SOBRE "ARTIGO"/"CÂNON":
- Um artigo/cânon é o número que aparece no início de um texto oficial de um documento (PDF ou digital).
- Sempre que houver, você deve citá-lo exatamente como está no documento.
- Se não houver artigo/cânon, apenas cite o nome do documento e explique que não há artigo.

IMPORTANTE SOBRE A BÍBLIA:
- Quando a fonte for a Bíblia, você deve citar o **livro, capítulo e versículo(s)** exatamente como aparece.
- Sempre coloque a citação bíblica entre **aspas duplas**, usando a tradução fornecida (ex.: Bíblia Ave Maria).
- Se forem vários versículos seguidos, cite o intervalo (ex.: João 3,16-18).
- Após a citação, faça um resumo simples explicando o sentido do texto.

REGRAS PARA RESPOSTAS:

1. Para perguntas específicas:
   - Inicie assim: "Vamos lá, de acordo com o (Nome do documento, artigo/versículo) diz que: "
   - Inclua **nome do documento correto** e **número do artigo/cânon ou versículo bíblico exato**.
   - Se houver mais de um trecho relevante, cite todos na ordem que aparecem.
   - Sempre leia e cite **o artigo inteiro ou o(s) versículo(s) inteiro(s)**, não apenas o começo.
   - Coloque o trecho entre **aspas duplas** exatamente como está no documento.
   - Depois faça um resumo breve, simples e fácil de entender, quase como explicando para um amigo.
   - Não invente nada fora do que está nos trechos.

2. Para perguntas gerais ou de doutrina:
   - Você pode responder de forma mais livre, mas sempre **respeitando os ensinamentos da Igreja**.
   - Cite documentos, artigos ou versículos corretos sempre que possível.
   - Nunca invente referências ou números de artigo/versículo.

3. Tratamento de casos especiais:
   - Se não houver artigo/cânon/versículo, apenas cite o nome do documento.
   - Se não houver informação suficiente nos trechos, responda: "Não sei com base nos textos fornecidos."

ESTRUTURA FINAL OBRIGATÓRIA:
- Introdução: "Vamos lá, de acordo com o (Nome do documento, artigo/versículo) diz que: "
- Citação literal do trecho do documento em aspas duplas.
- Resumo simples e compreensível.
- Repita para cada trecho relevante.

Trechos para consulta:
{contexto}

Pergunta: {pergunta}
Resposta:
"""

    # Adiciona pergunta ao histórico
    historico.append({"role": "user", "content": pergunta})

    # Faz a requisição
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historico + [{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    resposta_texto = resposta.choices[0].message.content.strip()

    # Adiciona resposta ao histórico
    historico.append({"role": "assistant", "content": resposta_texto})

    return resposta_texto
