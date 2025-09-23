from src.chat import responder_com_documentos

print("VoxAI iniciado! Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Pergunta: ")
    if pergunta.lower() == "sair":
        break
    resposta = responder_com_documentos(pergunta)
    print(f"\nVox: {resposta}\n")
