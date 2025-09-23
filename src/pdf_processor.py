import PyPDF2
import os
from src.config import PDF_PATH, CHUNK_SIZE

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with open(caminho_pdf, "rb") as arquivo:
        reader = PyPDF2.PdfReader(arquivo)
        for pagina in reader.pages:
            texto += pagina.extract_text() + "\n"
    return texto

def dividir_em_chunks(texto, tamanho=CHUNK_SIZE):
    palavras = texto.split()
    chunks = []
    for i in range(0, len(palavras), tamanho):
        chunks.append(" ".join(palavras[i:i+tamanho]))
    return chunks

def carregar_todos_pdfs():
    documentos = []
    for arquivo in os.listdir(PDF_PATH):
        if arquivo.endswith(".pdf"):
            texto = extrair_texto_pdf(os.path.join(PDF_PATH, arquivo))
            documentos.append({"nome": arquivo, "texto": texto})
    return documentos

def criar_trechos():
    documentos = carregar_todos_pdfs()
    trechos = []
    for doc in documentos:
        for chunk in dividir_em_chunks(doc["texto"]):
            trechos.append({"documento": doc["nome"], "texto": chunk})
    return trechos
