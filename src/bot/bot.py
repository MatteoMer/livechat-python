import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Discord bot token and ID from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ID = os.getenv("BOT_ID")
BACKEND_URL = os.getenv("BACKEND_URL")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

# Initialize bot and set command prefix
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Listen to a specific channel (you can specify the channel name)
    if message.channel.name == CHANNEL_NAME:
        if message.attachments:
            for attachment in message.attachments:
                media_url = attachment.url

                # Send media URL to FastAPI backend
                headers = {"x_bot_id": BOT_ID}

                response = requests.post(
                    "https://play-on-stream.onrender.com/new_media/",
                    json={
                        "media_url": media_url,
                        "message": message.content,
                    },
                    headers=headers,
                )

                if response.status_code == 200:
                    await message.channel.send("Media forwarded!")
                else:
                    await message.channel.send("Something went wrong.")


# Run the bot
bot.run(BOT_TOKEN)
