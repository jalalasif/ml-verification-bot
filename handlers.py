import discord
import random
import asyncio
from utils import (
    can_attempt_quiz,
    record_attempt,
    is_user_verified,
    get_remaining_attempts,
    get_role_names
)
from quiz import get_questions, shuffle_options

# Concurrency protection
active_quiz_users = set()
MAX_CONCURRENT_QUIZZES = 3

questions = get_questions()

async def handle_verification(ctx, bot, guild_id, welcome_channel_name, answer_log_category, answer_log_channel):
    member = ctx.author
    roles = get_role_names(member)

    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        print(f"[INFO] Tried to delete a message that no longer exists (ID: {ctx.message.id}).")
    except discord.errors.Forbidden:
        print(f"[WARNING] Missing permissions to delete message in #{ctx.channel.name}.")

    if "mod" in roles:
        pass
    elif "unverified" in roles and "comrade" not in roles:
        pass
    elif "comrade" in roles and "mod" not in roles:
        await ctx.send("You are already verified and cannot take the quiz again.")
        return
    else:
        await ctx.send("You are not permitted to take the verification quiz.")
        return

    if not can_attempt_quiz(member.id):
        await ctx.send("You have reached the maximum number of quiz attempts (6).")
        return

    if member.id in active_quiz_users:
        await ctx.send("You're already in a quiz session.")
        return

    if len(active_quiz_users) >= MAX_CONCURRENT_QUIZZES:
        await ctx.send("Too many users are currently taking the quiz. Please wait a moment and try again.")
        return

    active_quiz_users.add(member.id)

    try:
        dm_channel = await member.create_dm()
        await dm_channel.send(
            "Hello there, my cutesy comrade! You're about to begin a short quiz for a vibe check! "
            "You'll need 30/40 to pass. Answer with A, B, C, or D. You’ve got this - and we're rooting for you!"
        )
        print(f"[INFO] Sent quiz intro DM to {member.name}#{member.discriminator} ({member.id})")
    except discord.Forbidden:
        active_quiz_users.discard(member.id)
        await ctx.send("I couldn't DM you. Please enable DMs and try again.")
        return

    score = 0
    user_answers = []

    for idx, q in enumerate(questions, 1):
        q = shuffle_options(q)
        options = q["options"]
        letters = list(options.keys())

        formatted_options = "\n".join(f"{letter}. {options[letter][0]}" for letter in letters)
        question_text = f"**{q['question']}**\n{formatted_options}"
        await asyncio.sleep(0.5)

        try:
            await dm_channel.send(question_text)
        except discord.HTTPException as e:
            if e.status == 429:
                print("[RATE LIMITED] Message not sent due to Discord rate limit.")
            raise

        def check(m):
            return m.author == member and m.channel == dm_channel

        try:
            msg = await bot.wait_for("message", check=check, timeout=120)
        except discord.HTTPException as e:
            if isinstance(e, discord.errors.HTTPException) and e.status == 429:
                print(f"[RATE LIMIT] Discord 429 error: {e}")
            active_quiz_users.discard(member.id)
            return
        except asyncio.TimeoutError:
            await dm_channel.send("Oh no! Time's up! Try again later when you're ready, ok?")
            active_quiz_users.discard(member.id)
            return

        answer_letter = msg.content.strip().upper()

        if answer_letter in letters:
            selected = options[answer_letter]
            earned = selected[1]
            score += earned
            user_answers.append((idx, q["question"], selected[0], earned))
        else:
            await dm_channel.send("Oopsies! That wasn’t one of the options. Let's skip this one for now!")
            user_answers.append((idx, q["question"], msg.content.strip(), 0))

    record_attempt(member.id)

    if score >= 30:
        comrade_role = discord.utils.get(member.guild.roles, name="comrade")
        unverified_role = discord.utils.get(member.guild.roles, name="unverified")
        if comrade_role:
            await member.add_roles(comrade_role)
            if unverified_role and unverified_role in member.roles:
                await member.remove_roles(unverified_role)
            await dm_channel.send("Yippee! You passed with {}/40. Welcome to our little corner of summer and sunshine!".format(score))
        else:
            await dm_channel.send("You passed the quiz, but I couldn't find the **comrade** role to assign you.")
    else:
        remaining = get_remaining_attempts(member.id)
        await dm_channel.send(
            f"Uh oh, sorry but you scored {score}/40. Sadly, that's not quite enough to align with our ideological positions. "
            f"But don’t worry — you can try again! Second time's the charm! Or third? Maybe fourth....?\n"
            f"You have {remaining} attempt(s) left!"
        )

    await asyncio.sleep(3.0)
    log_channel = discord.utils.get(ctx.guild.text_channels, name="user-answers")
    if log_channel:
        summary_lines = [f"User: {member.name}#{member.discriminator}\n", "Answers:"]
        for idx, question, answer, points in user_answers:
            summary_lines.append(f"Q{idx}: {question} – \"{answer}\" : +{points}")
        summary_lines.append(f"\nTotal Score: {score}/40")

        try:
            await log_channel.send("\n".join(summary_lines))
        except discord.HTTPException as e:
            print(f"[ERROR] Failed to send quiz summary: {e}")

    active_quiz_users.discard(member.id)
