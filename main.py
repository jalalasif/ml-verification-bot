import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from handlers import handle_verification

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1313265229228015646
WELCOME_CHANNEL_NAME = "welcome"
ANSWER_LOG_CATEGORY = "admin & rules"
ANSWER_LOG_CHANNEL = "user-answers"

app = Flask('')

@app.route('/')
def home():
    return "ML Vetting Bot is awake and running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

@bot.command(name="verifyme")
@commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
async def verifyme(ctx):
    await handle_verification(ctx, bot, GUILD_ID, WELCOME_CHANNEL_NAME, ANSWER_LOG_CATEGORY, ANSWER_LOG_CHANNEL)

keep_alive()
print(f"Loaded token: {'yes' if TOKEN else 'no'}")
bot.run(TOKEN)