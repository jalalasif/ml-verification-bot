# Discord Verification Bot

This is a modular Python-based Discord bot designed to verify new users through a short, friendly DM-based quiz. Instead of testing for objective "correctness," the quiz gauges a user's ideological alignment and vibe fit with your community, using a weighted answer system. It’s playful, thoughtful, and built to scale safely.

## ✨ Features

- **Private DM-based quiz delivery**  
  Users type `!verifyme` in a designated channel, triggering a private 8-question multiple-choice quiz via DM.

- **Ideological scoring, not correctness**  
  Each question offers four plausible answers with different point values. All are technically valid, but some align more with the community's worldview. Users need **30 out of 40 points** to pass.

- **Randomized questions and shuffled answers**  
  Both the question order and the answer choices are randomized each time, making every session unique and preventing gaming.

- **Lenient answer input**  
  Users can respond with `A`, `B`, `C`, or `D` (case-insensitive). Invalid inputs are gracefully skipped with no crashes.

- **Attempts capped per user**  
  Users may take the quiz up to **6 times per day**, tracked by user ID and date. Attempts are stored in a local `attempts.json` file.

- **Channel-restricted activation**  
  The quiz can only be launched from a designated channel (e.g., `start-here-for-verification`) to maintain order and avoid abuse.

- **Role-based access control**  
  - Users with `mod` role: always allowed  
  - Users with `unverified` role and not `comrade`: allowed  
  - Users with `comrade` but not `mod`: denied  
  - All others: denied  

- **Automated scoring with cozy feedback**  
  After answering all questions, users get a personalized, encouraging summary of their score and whether they passed or not.

- **Friendly timeout handling**  
  If the user takes more than 2 minutes to answer a question, the bot gently cancels the quiz and invites them to try again later.

- **Public result logging**  
  After each quiz, a summary is posted to the `#user-answers` channel for transparency. It includes all user responses, earned points, and score.

- **Warm and playful UX**  
  Messages sent to users use cheerful, gender-inclusive, encouraging language to make the verification experience delightful.

## 🛡️ Rate Limiting Protections

To avoid Discord rate-limit bans and ensure stability:

- Only **3 users** can take the quiz concurrently
- 0.5 second delay added before sending each question
- Total messages are paced and spaced carefully
- Post-quiz logs are delayed by a few seconds before sending
- Users cannot trigger multiple quizzes simultaneously
- The `!verifyme` command has a short cooldown lock (2s between invocations)
- Graceful error handling for 429 errors and DM issues

## 🚀 Hosting & Uptime

The bot is deployed as a **Web Service on [Render](https://render.com)** and kept alive using regular pings from [Uptime Robot](https://uptimerobot.com) every 5 minutes. A lightweight Flask server handles these keep-alive pings.

## 🛠️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/jalalasif/discord-verification-bot.git
cd discord-verification-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment

Create a `.env` file or configure Render environment variables:

```
DISCORD_TOKEN=your-bot-token-here
GUILD_ID=your-discord-guild-id
```

### 4. Deploy to Render

- Create a **Web Service** on Render
- Use `python main.py` as your start command
- Add `DISCORD_TOKEN` and `GUILD_ID` to environment variables
- Render will generate a public URL for your Flask uptime endpoint

### 5. Set up Uptime Robot

- Go to [https://uptimerobot.com](https://uptimerobot.com)
- Create a new monitor (HTTP/S type)
- Point it to your Render URL (e.g., `https://your-bot.onrender.com`)
- Set the interval to **every 5 minutes**

## 🔧 Server Configuration

Your server must include:

- A role named `comrade` (post-verification role)
- A role named `unverified`
- A role named `mod` (admin/verification override)
- A text channel named `start-here-for-verification`
- A text channel named `user-answers` (under any category)

**Important:** Names are case-sensitive and must match exactly.

## 📁 File Structure

```
discord-verification-bot/
├── main.py             # Command routing and role logic
├── handlers.py         # Quiz session flow and score logic
├── quiz.py             # Loads quiz data and shuffles options
├── utils.py            # Attempt tracking and role parsing
├── quiz.json           # All quiz content (questions and answer weights)
├── messages.json       # Optional welcome messages (future use)
├── keep_alive.py       # Flask server for uptime
├── attempts.json       # Per-user daily attempt tracking
├── requirements.txt    # Dependency list
└── README.md           # This file
```

## 🪪 License

This project is licensed under the MIT License. See `LICENSE` for full details.