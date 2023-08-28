from fastapi import FastAPI, WebSocket, HTTPException, Header
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve environment variables
DISCORD_BOT_ID = os.getenv("DISCORD_BOT_ID")


# Create a data model for incoming media
class Body(BaseModel):
    media_url: str
    message: str


# In-memory storage for media; in a real-world app, you'd use a database
media_storage: List[str] = []

# In-memory list to keep track of connected WebSocket clients
connected_clients = []


@app.post("/new_media/")
async def new_media(body: Body, x_bot_id: str = Header(None)):
    # Check if the request is coming from the authorized bot
    # print(x_bot_id, DISCORD_BOT_ID)
    # if x_bot_id != DISCORD_BOT_ID:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    # Add the media URL to storage
    media_storage.append(body.media_url)
    media_storage.append(body.message)
    print("noway")

    # Notify all connected WebSocket clients about the new media
    for client in connected_clients:
        print(body.message)
        await client.send_json(
            {
                "action": "new_media",
                "media_url": body.media_url,
                "message": body.message,
            }
        )

    return {"message": "Media received"}


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # You can add code here to handle incoming WebSocket messages if needed

    except:
        # Remove the WebSocket client if it disconnects
        connected_clients.remove(websocket)
