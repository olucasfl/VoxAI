from openai import OpenAI
from .embeddings import preparar_embeddings
from .config import TOP_K, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

embeddings, trechos = preparar_embeddings()

def buscar_trechos(pergunta):
    # Gerar embedding da pergunta
    pergunta_emb = client.embeddings.create(
        model="text-embedding-ada-002",
        input=pergunta
    ).data[0].embedding

    # Calcular similaridade (cosine)
    import numpy as np
    def cosine(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    scores = [cosine(pergunta_emb, emb) for emb in embeddings]
    idx_top = np.argsort(scores)[-TOP_K:][::-1]
    return [trechos[i] for i in idx_top]
