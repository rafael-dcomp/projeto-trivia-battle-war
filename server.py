from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import json

app = FastAPI()

# Perguntas e respostas em memória
questions = [
    {"question": "Qual é o maior planeta do sistema solar?",
     "options": ["Terra", "Marte", "Júpiter", "Saturno"],
     "answer": 2},

    {"question": "Quem escreveu 'Dom Quixote'?",
     "options": ["Machado de Assis", "Miguel de Cervantes", "William Shakespeare", "José Saramago"],
     "answer": 1},

    {"question": "Qual é o símbolo químico do ouro?",
     "options": ["Au", "Ag", "Fe", "Hg"],
     "answer": 0},

    {"question": "Em que ano aconteceu a Independência do Brasil?",
     "options": ["1500", "1822", "1889", "1945"],
     "answer": 1},

    {"question": "Qual é o time com mais títulos da Copa do Mundo?",
     "options": ["Brasil", "Alemanha", "Itália", "Argentina"],
     "answer": 0}
]

rooms: dict[str, list] = {}


@app.get("/")
async def get():
    with open("index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@app.get("/quiz.html")
async def get_quiz():
    with open("quiz.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@app.get("/multiplayer.html")
async def get_multiplayer():
    with open("multiplayer.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@app.get("/sobre.html")
async def get_quiz():
    with open("sobre.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@app.get("/game.html")
async def get_game():
    with open("game.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = eval(data)  # Use json.loads(data) para mais segurança

            action = message.get("action")
            # Converter para string por segurança
            room_code = str(message.get("roomCode"))

            if action == "create":
                if room_code not in rooms:
                    rooms[room_code] = []  # Criar a sala
                    await websocket.send_json({"status": "success", "message": "Sala criada!"})
                else:
                    await websocket.send_json({"status": "error", "message": "Sala já existe!"})

            elif action == "join":
                if room_code in rooms:
                    if len(rooms[room_code]) < 2:
                        rooms[room_code].append(websocket)
                        await websocket.send_json({"status": "success", "message": "Entrou na sala!"})

                        if len(rooms[room_code]) == 2:
                            # Notificar ambos os jogadores para iniciar o jogo
                            for ws in rooms[room_code]:
                                await ws.send_json({"status": "start_game", "message": "Jogo iniciando!"})
                    else:
                        await websocket.send_json({"status": "error", "message": "Sala cheia!"})
                else:
                    await websocket.send_json({"status": "error", "message": "Sala não encontrada!"})

            elif action == "get_questions":
                await websocket.send_json({"action": "load_questions", "questions": questions})
            elif action == "answer":
                selected_answer = message.get("answer")
                question_index = message.get("question_index")

                if questions[question_index]["answer"] == selected_answer:
                    if websocket == player1_ws:
                        player_scores[player1_ws] += 1
                    elif websocket == player2_ws:
                        player_scores[player2_ws] += 1

    # Envia a atualização do placar para ambos os jogadores
                await player1_ws.send_json({
                    "action": "update_score",
                    "player1Score": player_scores.get(player1_ws, 0),
                    "player2Score": player_scores.get(player2_ws, 0)
                })

                await player2_ws.send_json({
                    "action": "update_score",
                    "player1Score": player_scores.get(player1_ws, 0),
                    "player2Score": player_scores.get(player2_ws, 0)
                })
    except WebSocketDisconnect:
        print("Cliente desconectado.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
