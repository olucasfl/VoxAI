from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.chat import responder_com_documentos  # usa sua função já pronta

app = FastAPI()

# Liberar acesso ao frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    pergunta: str

@app.post("/perguntar")
def perguntar(req: Pergunta):
    resposta = responder_com_documentos(req.pergunta)
    return {"resposta": resposta}
