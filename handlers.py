import discord
import random
from quiz import load_quiz, shuffle_options
from utils import load_welcome_messages, can_attempt, record_attempt

QUIZ = load_quiz()
WELCOME_MESSAGES = load_welcome_messages()
ALLOWED_CHANNELS = {"start-here-for-verification", "polls-and-tests", "unverified"}

async def handle_verification(ctx, bot, GUILD_ID, WELCOME_CHANNEL_NAME, ANSWER_LOG_CATEGORY, ANSWER_LOG_CHANNEL):
    if ctx.channel.name not in ALLOWED_CHANNELS:
        await ctx.send(f"{ctx.author.mention} You can only use this command in the designated verification channels (#polls-and-tests & #start-here-for-verification)!")
        return

    if not can_attempt(ctx.author.id):
        await ctx.send(f"{ctx.author.mention} You've reached the max number of quiz attempts today. Please try again tomorrow!")
        return

    await ctx.message.delete()
    try:
        await ctx.author.send("Hello there, my cutesy comrade! You're about to begin a short quiz for a vibe check! You'll need 30/40 to pass. Answer with A, B, C, or D. You’ve got this - and we're rooting for you!")
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
            msg = await bot.wait_for("message", timeout=240.0, check=check)
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
            await ctx.author.send("Oh no! Time's up! Try again later when you're ready, ok?")
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

    # Check if user already has comrade role
    has_comrade = comrade_role in member.roles if comrade_role else False

    if score >= 30:
        await ctx.author.send(f"Yippee! You passed with {score}/40. Welcome to our little corner of summer and sunshine!")
        if not has_comrade and comrade_role:
            await member.add_roles(comrade_role)
            if unverified_role and unverified_role in member.roles:
                await member.remove_roles(unverified_role)
            if welcome_channel:
                await welcome_channel.send(f"{random.choice(WELCOME_MESSAGES)} {member.mention}")
    else:
        await ctx.author.send(f"Uh oh, sorry but you scored {score}/40. Sadly, that's not quite enough to align with our ideological positions. But don’t worry — you can try again! Second time's the charm! Or third? Maybe fourth....?")

    # Send answer breakdown if user already had comrade role or passed successfully
    if has_comrade or score >= 30:
        try:
            if score >= 30:
                breakdown_intro = "📊 You did it! I'd give you a high five, but I'm just a bot lol! Anyway, here's your quiz breakdown:"
            else:
                breakdown_intro = "📊 Thanks for giving it a shot! Since you're already verified, here's your quiz breakdown:"
            await ctx.author.send(f"{breakdown_intro}\n\n{summary}")
        except discord.Forbidden:
            print(f"Could not send breakdown DM to {ctx.author.name}")