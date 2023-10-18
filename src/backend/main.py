from fastapi import FastAPI, WebSocket, HTTPException, Header
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from urllib.parse import urlsplit

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


def remove_url_parameters(url: str) -> str:
    # Using urlsplit to break down the URL into its components, then rebuild it without the query part
    url_parts = urlsplit(url)
    clean_url = url_parts._replace(query="")
    return clean_url.geturl()


@app.post("/new_media/")
async def new_media(body: Body, x_bot_id: str = Header(None)):
    # Check if the request is coming from the authorized bot
    # if x_bot_id != DISCORD_BOT_ID:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

    # Clean the media URL
    clean_media_url = remove_url_parameters(body.media_url)

    # Add the cleaned media URL to storage
    media_storage.append(clean_media_url)
    media_storage.append(body.message)
    print("noway")

    # Notify all connected WebSocket clients about the new media
    for client in connected_clients:
        print(body.message)
        await client.send_json(
            {
                "action": "new_media",
                "media_url": clean_media_url,
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
