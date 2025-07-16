# Load environment variables and required modules
import asyncio
from datetime import datetime, timedelta
last_verification_time = None
verification_lock = asyncio.Lock()

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
from handlers import handle_verification

# Load .env values
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# Roles
BLOCKED_ROLE = "comrade"
ALLOWED_ROLES = ["unverified", "mod"]

# Channels
WELCOME_CHANNEL_NAME = "start-here-for-verification"

# Set up bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")

@bot.command()
async def verifyme(ctx):
    global last_verification_time
    
    if not ctx.guild:
        return  # Ignore DMs

    # Restrict command to designated channel only
    if ctx.channel.name != WELCOME_CHANNEL_NAME:
        await ctx.send("Please use the designated channel for verification.")
        return
        
    async with verification_lock:
        now = datetime.utcnow()
        if last_verification_time and (now - last_verification_time) < timedelta(seconds=2):
            await ctx.send("Too many verifications at once. Please wait a moment and try again.")
            return
        last_verification_time = now

    member = ctx.author
    roles = [role.name.lower() for role in member.roles]

    # Access logic:
    # Rule 1: If user has mod, allow no matter what
    if "mod" in roles:
        pass

    # Rule 2: If user has unverified and not comrade, allow
    elif "unverified" in roles and BLOCKED_ROLE not in roles:
        pass

    # Rule 3: If user has comrade but not mod, deny
    elif BLOCKED_ROLE in roles and "mod" not in roles:
        await ctx.send("You are already verified and cannot take the quiz again.")
        return

    # Rule 4: All others denied
    else:
        await ctx.send("You are not eligible to verify.")
        return

    # Cleanup command message
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    await handle_verification(ctx, bot, GUILD_ID, WELCOME_CHANNEL_NAME, None, None)

# Keep bot alive
keep_alive()
bot.run(TOKEN)
