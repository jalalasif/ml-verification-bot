import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 🔐 Token from Render Secrets
TOKEN = os.getenv("DISCORD_TOKEN")

# ✅ Your Server (Guild) ID
GUILD_ID = 1313265229228015646

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

# 🧠 Quiz content
quiz = [
    {
        "question": "What is the fundamental contradiction within capitalism?",
        "options": {
            "A": ("The tension between rich and poor due to unfair policies", 3),
            "B": ("The contradiction between the socialized nature of production and private appropriation of profit", 5),
            "C": ("The problem of market inefficiencies and poor regulation", 0),
            "D": ("The individual’s struggle to find meaning in a consumer society", 0)
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
        "question": "What is the purpose of the state in class society?",
        "options": {
            "A": ("To enforce laws and maintain social order", 0),
            "B": ("To provide services and protect citizens", 3),
            "C": ("To mediate class conflicts fairly", 0),
            "D": ("To serve as an instrument of class rule, upholding the interests of the ruling class", 5)
        }
    },
    {
        "question": "What defines class in Marxist theory?",
        "options": {
            "A": ("Cultural background and education", 0),
            "B": ("Relative income and social status", 3),
            "C": ("Relationship to the means of production", 5),
            "D": ("Level of political engagement", 0)
        }
    },
    {
        "question": "Which of these is a necessary condition for the dictatorship of the proletariat?",
        "options": {
            "A": ("Free press and multiparty competition", 0),
            "B": ("Workers seizing state power and suppressing counterrevolution", 5),
            "C": ("Decentralized communes and nonviolence", 3),
            "D": ("Gradual reform through parliamentary means", 0)
        }
    },
    {
        "question": "What best describes imperialism today?",
        "options": {
            "A": ("A relic of the colonial past with little modern relevance", 0),
            "B": ("Aggressive military expansionism by rogue states", 3),
            "C": ("The highest stage of capitalism, marked by monopolies and export of capital", 5),
            "D": ("A geopolitical competition between great powers", 3)
        }
    },
    {
        "question": "What role should the working class in imperialist countries play?",
        "options": {
            "A": ("Demand better wages and conditions through unions", 3),
            "B": ("Focus on domestic justice before international issues", 0),
            "C": ("Stand in solidarity with the global proletariat and actively oppose their own ruling class’s imperialism", 5),
            "D": ("Support ethical foreign policy and fair trade initiatives", 0)
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
            role = discord.utils.get(guild.roles, name="comrade")
            if member and role:
                await member.add_roles(role)
                await ctx.author.send("🎉 You’ve been given the **comrade** role.")
            else:
                await ctx.author.send("⚠️ Could not find you or the role on the server.")
        except Exception as e:
            await ctx.author.send(f"❗ Error assigning your role:\n{e}")
    else:
        await ctx.author.send(f"❌ You scored {score}/40. That doesn’t meet the threshold for entry.\nFeel free to try again later.")

# 🔁 Start the web server to stay alive via UptimeRobot
keep_alive()
bot.run(TOKEN)
