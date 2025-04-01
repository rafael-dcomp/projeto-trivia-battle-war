
import asyncio
import websockets
import json


async def connect_to_server():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            question_data = await websocket.recv()
            question = json.loads(question_data)
            # Atualizar a interface do jogo com a nova pergunta
