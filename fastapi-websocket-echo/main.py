from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Server received: {message}")
    
    except WebSocketDisconnect:
        print("Client disconnected")