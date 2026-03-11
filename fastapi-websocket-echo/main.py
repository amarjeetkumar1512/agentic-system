from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h2>WebSocket Echo Test</h2>

    <input id="messageInput" type="text" placeholder="Enter message">
    <button onclick="sendMessage()">Send</button>

    <h3>Messages</h3>
    <ul id="messages"></ul>

    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            const li = document.createElement("li");
            li.textContent = event.data;
            document.getElementById("messages").appendChild(li);
        };

        function sendMessage() {
            const input = document.getElementById("messageInput");
            ws.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>

"""

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Server received: {message}")
    
    except WebSocketDisconnect:
        print("Client disconnected")