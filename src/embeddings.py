import os
import pickle
from .config import OPENAI_API_KEY, EMBEDDINGS_PATH
from .pdf_processor import criar_trechos
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

def gerar_embedding(texto):
    resposta = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texto
    )
    return resposta.data[0].embedding

def criar_embeddings(trechos):
    embeddings = []
    for chunk in trechos:
        emb = gerar_embedding(chunk["texto"])
        embeddings.append(emb)
    return embeddings

def salvar_embeddings(embeddings, trechos):
    os.makedirs(os.path.dirname(EMBEDDINGS_PATH), exist_ok=True)
    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump({"embeddings": embeddings, "trechos": trechos}, f)

def carregar_embeddings():
    if os.path.exists(EMBEDDINGS_PATH) and os.path.getsize(EMBEDDINGS_PATH) > 0:
        with open(EMBEDDINGS_PATH, "rb") as f:
            data = pickle.load(f)
        return data["embeddings"], data["trechos"]
    return None, None

def preparar_embeddings():
    embeddings, trechos = carregar_embeddings()
    if embeddings is None:
        trechos = criar_trechos()
        embeddings = criar_embeddings(trechos)
        salvar_embeddings(embeddings, trechos)
    return embeddings, trechos
