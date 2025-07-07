import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 🔐 Token from Render Secrets
TOKEN = os.getenv("DISCORD_TOKEN")

# ✅ Your Server (Guild) ID
GUILD_ID = 1313265229228015646

# 💬 Name of the welcome channel to post alerts in
WELCOME_CHANNEL_NAME = "welcome"

# 🌐 Flask server to keep bot alive
app = Flask('')

@app.route('/')
def home():
    return "✅ ML Vetting Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🧠 Enable required intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🧠 Refined quiz content
quiz = [
    {
        "question": "What is the core contradiction that ultimately destabilizes capitalism from within?",
        "options": {
            "A": ("Persistent inequality between rich and poor resulting from flawed policies", 3),
            "B": ("The conflict between collective labor that creates value and the private ownership that extracts it", 5),
            "C": ("Excess consumerism leading to ecological and psychological crises", 0),
            "D": ("The lack of sufficient regulations to stabilize market competition", 0)
        }
    },
    {
        "question": "How should LGBTQ+ liberation be understood within Marxist-Leninist political struggle?",
        "options": {
            "A": ("It is an essential part of dismantling capitalist social structures and must be integrated into proletarian revolution", 5),
            "B": ("It’s important, but best pursued after the primary class struggle is won", 3),
            "C": ("It is largely a cultural concern, not directly tied to material liberation", 0),
            "D": ("It has been co-opted by neoliberal elites to weaken working-class unity", -5)
        }
    },
    {
        "question": "Which best reflects a revolutionary attitude toward queer and trans comrades?",
        "options": {
            "A": ("They are integral members of the proletariat whose liberation cannot be separated from the class struggle", 5),
            "B": ("They should be included, but not prioritized, to avoid alienating more traditional workers", 3),
            "C": ("They often bring unnecessary division to organizing spaces", 0),
            "D": ("Their visibility is a result of bourgeois decadence and must be tempered", -5)
        }
    },
    {
        "question": "What is the state's function in a society structured by class antagonisms?",
        "options": {
            "A": ("A neutral body that arbitrates between competing interests to maintain harmony", 0),
            "B": ("A reflection of the dominant culture's moral consensus", 0),
            "C": ("A tool that ensures social services and legal equality across classes", 3),
            "D": ("A coercive apparatus used to maintain the dominance of the ruling class", 5)
        }
    },
    {
        "question": "According to Marxist analysis, how are social classes primarily determined?",
        "options": {
            "A": ("Levels of education, upbringing, and cultural capital", 0),
            "B": ("Wealth brackets and perceived social mobility", 3),
            "C": ("One’s position in relation to control over productive property", 5),
            "D": ("Degree of participation in democratic processes", 0)
        }
    },
    {
        "question": "What precondition is necessary to secure and maintain proletarian political power?",
        "options": {
            "A": ("A robust and independent press to expose abuses of power", 0),
            "B": ("Mass mobilization of workers to seize the state and suppress counter-revolution", 5),
            "C": ("Consensus-building through participatory local governance", 3),
            "D": ("Electoral competition that keeps leadership accountable", 0)
        }
    },
    {
        "question": "How should we best understand imperialism in our current global moment?",
        "options": {
            "A": ("Primarily as a moral failure of powerful nations to respect sovereignty", 0),
            "B": ("The extension of military dominance by undemocratic regimes", 3),
            "C": ("The global stage of monopoly capitalism, exporting capital and securing superprofits abroad", 5),
            "D": ("Strategic rivalries between blocs that vie for regional influence", 3)
        }
    },
    {
        "question": "What role ought workers in core imperialist nations play in global class struggle?",
        "options": {
            "A": ("Organize at home while encouraging responsible global policy", 0),
            "B": ("Prioritize domestic reform efforts before worrying about the international sphere", 0),
            "C": ("Reject their own ruling class’s imperialism and unite with workers of the global South", 5),
            "D": ("Push for fair trade and diplomacy to reduce exploitation abroad", 3)
        }
    }
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

@bot.command(name="verifyme")
async def verify(ctx):
    await ctx.message.delete()
    try:
        await ctx.author.send("📜 Welcome to the verification quiz. You'll get 8 questions. Reply with A, B, C, or D.\nYou need at least 30/40 to join. Let’s begin!")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, please enable DMs from server members to complete verification.")
        return

    score = 0

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    for q in quiz:
        q_text = f"\n**{q['question']}**\n"
        for letter, (text, _) in q["options"].items():
            q_text += f"{letter}. {text}\n"
        await ctx.author.send(q_text)

        try:
            msg = await bot.wait_for('message', timeout=120.0, check=check)
            choice = msg.content.upper().strip()
            if choice in q["options"]:
                score += q["options"][choice][1]
            else:
                await ctx.author.send("❌ Invalid response. Skipping this question.")
        except Exception:
            await ctx.author.send("⏱️ Time's up. Verification canceled.")
            return

    if score >= 30:
        await ctx.author.send(f"✅ You passed with {score}/40. Welcome, comrade!")

        guild = bot.get_guild(GUILD_ID)
        if not guild:
            await ctx.author.send("⚠️ Bot couldn't access the server to assign your role.")
            return

        try:
            member = await guild.fetch_member(ctx.author.id)
            comrade_role = discord.utils.get(guild.roles, name="comrade")
            unverified_role = discord.utils.get(guild.roles, name="unverified")
            welcome_channel = discord.utils.get(guild.text_channels, name=WELCOME_CHANNEL_NAME)

            if member and comrade_role:
                await member.add_roles(comrade_role)
                if unverified_role in member.roles:
                    await member.remove_roles(unverified_role)
                await ctx.author.send("🎉 You’ve been given the **comrade** role and removed from **unverified**.")
                if welcome_channel:
                    await welcome_channel.send(f"🎉 Welcome {member.mention}! Verified and ready to roll.")
            else:
                await ctx.author.send("⚠️ Could not find you or the required roles on the server.")
        except Exception as e:
            await ctx.author.send(f"❗ Error assigning your role:\n{e}")
    else:
        await ctx.author.send(f"❌ You scored {score}/40. That doesn’t meet the threshold for entry.\nFeel free to try again later.")

# 🔁 Start the web server to stay alive via UptimeRobot
keep_alive()
bot.run(TOKEN)
