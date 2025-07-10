import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread
import random

# Secret token for bot authentication
TOKEN = os.getenv("DISCORD_TOKEN")

# Server and channel configuration
GUILD_ID = 1313265229228015646
WELCOME_CHANNEL_NAME = "welcome"
ANSWER_LOG_CHANNEL = "user-answers"
ANSWER_LOG_CATEGORY = "admin & rules"

# Flask app to keep the bot alive
app = Flask('')

@app.route('/')
def home():
    return "ML Vetting Bot is humming happily and very much alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Discord bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Quiz content
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

# Welcome messages pool
welcome_messages = [
    "Say hello to our newest comrade! You passed the vibe and theory check. Welcome aboard.",
    "Another beautiful brain just joined us. Let’s give a big warm welcome to our comrade.",
    "Revolutionary spirit detected. Welcome to the collective, comrade.",
    "A fresh comrade has arrived! Give them some love and solidarity.",
    "They studied, they slayed, and now they’re here. Welcome to the revolution."
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} and floating happily")

@bot.command(name="verifyme")
async def verify(ctx):
    await ctx.message.delete()
    try:
        await ctx.author.send("Hi there! You’re about to start a little quiz that helps us keep this space thoughtful and safe. Eight questions. Be honest, take your time, and just answer A, B, C, or D. You’ll need 30 points to pass. You got this.")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, please turn on your DMs so I can float into your inbox")
        return

    score = 0
    answers = []
    shuffled_quiz = quiz.copy()
    random.shuffle(shuffled_quiz)

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    for idx, q in enumerate(shuffled_quiz, start=1):
        q_text = f"\n**{q['question']}**\n"
        for letter, (text, _) in q["options"].items():
            q_text += f"{letter}. {text}\n"
        await ctx.author.send(q_text)

        try:
            msg = await bot.wait_for('message', timeout=120.0, check=check)
            choice = msg.content.upper().strip()

            correct_letter = max(q["options"], key=lambda k: q["options"][k][1])
            correct_score = q["options"][correct_letter][1]

            if choice in q["options"]:
                user_score = q["options"][choice][1]
                score += user_score

                if user_score == correct_score:
                    answers.append(f"{idx}. {choice} ✓")
                else:
                    correct_text = f"{correct_letter} ({q['options'][correct_letter][0]})"
                    answers.append(f"{idx}. {choice} ✗ — correct answer: {correct_text}")
            else:
                await ctx.author.send("That wasn’t a valid answer sweetie, but no worries, we’re skipping it")
                correct_text = f"{correct_letter} ({q['options'][correct_letter][0]})"
                answers.append(f"{idx}. Invalid ✗ — correct answer: {correct_text}")
        except Exception:
            await ctx.author.send("Hmm, looks like we ran out of time. That’s okay! Feel free to try again later")
            return

    summary = "\n".join(answers)
    total_summary = f"User: {ctx.author} ({ctx.author.id})\nAnswers:\n{summary}\nScore: {score}/40"

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        await ctx.author.send("Hmm, I couldn’t reach the server. Something’s off")
        return

    try:
        member = await guild.fetch_member(ctx.author.id)
        comrade_role = discord.utils.get(guild.roles, name="comrade")
        unverified_role = discord.utils.get(guild.roles, name="unverified")
        welcome_channel = discord.utils.get(guild.text_channels, name=WELCOME_CHANNEL_NAME)

        category = discord.utils.get(guild.categories, name=ANSWER_LOG_CATEGORY)
        log_channel = None
        if category:
            log_channel = discord.utils.get(category.channels, name=ANSWER_LOG_CHANNEL)

        if log_channel:
            await log_channel.send(total_summary)

        if score >= 30:
            await ctx.author.send(f"You did it! Your score was {score}/40 and that means you passed! We’re so happy to have you here")
            if member and comrade_role:
                await member.add_roles(comrade_role)
                if unverified_role in member.roles:
                    await member.remove_roles(unverified_role)
                await ctx.author.send("All done! You’ve got your comrade role now. Feel free to look around and get cozy")
                if welcome_channel:
                    welcome_text = random.choice(welcome_messages)
                    await welcome_channel.send(f"{welcome_text} {member.mention}")
            else:
                await ctx.author.send("Something glitched when assigning your role. Let someone know and we’ll fix it")
        else:
            await ctx.author.send(f"Hey, your score was {score}/40 which doesn’t meet the entry mark. That’s okay though — this quiz is meant to challenge. You’re totally welcome to try again later when you feel ready")
    except Exception as e:
        await ctx.author.send(f"Oopsie, something broke during the final steps:\n{e}")

keep_alive()
bot.run(TOKEN)
