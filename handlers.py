import discord
import random
from quiz import load_quiz, shuffle_options
from utils import load_welcome_messages, can_attempt, record_attempt

QUIZ = load_quiz()
WELCOME_MESSAGES = load_welcome_messages()
ALLOWED_CHANNELS = {"start-here-for-verification", "polls-and-tests"}

async def handle_verification(ctx, bot, GUILD_ID, WELCOME_CHANNEL_NAME, ANSWER_LOG_CATEGORY, ANSWER_LOG_CHANNEL):
    if ctx.channel.name not in ALLOWED_CHANNELS:
        await ctx.send(f"{ctx.author.mention} You can only use this command in the designated verification channels.")
        return

    if not can_attempt(ctx.author.id):
        await ctx.send(f"{ctx.author.mention} You've reached the max number of quiz attempts today. Please try again tomorrow.")
        return

    await ctx.message.delete()
    try:
        await ctx.author.send("Hi! You're about to begin a short quiz. You'll need 30/40 to pass. Answer with A, B, C, or D. You’ve got this!")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention}, please enable DMs so I can send you the quiz.")
        return

    score = 0
    answers = []
    questions = [shuffle_options(q) for q in random.sample(QUIZ, len(QUIZ))]

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    for idx, q in enumerate(questions, start=1):
        text = f"\n**{q['question']}**\n"
        for letter, (desc, _) in q["options"].items():
            text += f"{letter}. {desc}\n"
        await ctx.author.send(text)

        try:
            msg = await bot.wait_for("message", timeout=120.0, check=check)
            choice = msg.content.upper().strip()

            correct_letter = max(q["options"], key=lambda k: q["options"][k][1])
            correct_text = f"{correct_letter} ({q['options'][correct_letter][0]})"

            if choice in q["options"]:
                points = q["options"][choice][1]
                score += points
                if choice == correct_letter:
                    answers.append(f"{idx}. {q['question']} — {choice} ✓")
                else:
                    answers.append(f"{idx}. {q['question']} — {choice} ✗ — correct: {correct_text}")
            else:
                answers.append(f"{idx}. {q['question']} — Invalid ✗ — correct: {correct_text}")
        except Exception:
            await ctx.author.send("Time's up! Try again later when you're ready.")
            return

    record_attempt(ctx.author.id)
    summary = "\n".join(answers)
    total_summary = f"User: {ctx.author} ({ctx.author.id})\nAnswers:\n{summary}\nScore: {score}/40"

    guild = bot.get_guild(GUILD_ID)
    member = await guild.fetch_member(ctx.author.id)
    comrade_role = discord.utils.get(guild.roles, name="comrade")
    unverified_role = discord.utils.get(guild.roles, name="unverified")
    welcome_channel = discord.utils.get(guild.text_channels, name=WELCOME_CHANNEL_NAME)

    log_channel = None
    category = discord.utils.get(guild.categories, name=ANSWER_LOG_CATEGORY)
    if category:
        log_channel = discord.utils.get(category.channels, name=ANSWER_LOG_CHANNEL)
    if log_channel:
        await log_channel.send(total_summary)

    if score >= 30:
        await ctx.author.send(f"You passed with {score}/40. Welcome!")
        if member and comrade_role:
            await member.add_roles(comrade_role)
            if unverified_role and unverified_role in member.roles:
                await member.remove_roles(unverified_role)
            if welcome_channel:
                await welcome_channel.send(f"{random.choice(WELCOME_MESSAGES)} {member.mention}")
    else:
        await ctx.author.send(f"You scored {score}/40. That's not quite enough. But don’t worry — you can try again later!")