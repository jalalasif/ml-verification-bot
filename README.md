# Discord Verification Bot

This is a modular Python-based Discord bot built to automate user verification through a lightweight quiz system. It ensures that new members meet a baseline level of understanding or alignment with community values before being granted access to the rest of the server.

## Features

- **Private DM-based quiz delivery**  
  When users type `!verifyme` in a designated channel, the bot initiates a private 8-question multiple-choice quiz.

- **Randomized questions and answers**  
  Both the order of questions and the order of their answer choices are shuffled each time, ensuring each attempt is unique.

- **Automated scoring with explanation**  
  Responses are scored in real time, with incorrect answers followed by a message showing the correct response and question. Passing score is 30 out of 40.

- **Attempt tracking and retry limit**  
  Users are limited to four attempts per 24 hours. Any additional attempts are gracefully denied with a friendly message.

- **Channel-restricted activation**  
  The quiz can only be launched from specific channels (e.g., `start-here-for-verification` or `polls-and-tests`) to maintain order and prevent misuse.

- **Role assignment on success**  
  Successful users are automatically assigned a pre-defined role (e.g., `comrade`) and have the `unverified` role removed.

- **Personalized welcome messages**  
  Upon passing, users are welcomed in a public `#welcome` channel using one of several randomly selected messages stored in a JSON file.

- **Answer logging for moderators**  
  All quiz answers, scores, and pass/fail status are posted to a private logging channel (`#user-answers`) nested under a category named `admin & rules`.

- **Friendly UX with timeout handling**  
  If a user does not respond within the time limit, the bot exits the quiz session politely and encourages them to try again later.

## Hosting & Uptime

The bot is deployed as an **active Web Service on [Render](https://render.com)** and kept alive using regular pings from [Uptime Robot](https://uptimerobot.com). A small Flask server is used to expose a status endpoint so Render does not suspend the instance due to inactivity.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/jalalasif/discord-verification-bot.git
cd discord-verification-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables

Set the following environment variable (either in a `.env` file or your hosting dashboard):

```
DISCORD_TOKEN=your-bot-token-here
```

### 4. Deploy to Render

- Create a **Web Service** on Render
- Use `python main.py` as your start command
- Set `DISCORD_TOKEN` in your Render environment variables
- Render will provide a public URL for your Flask endpoint

### 5. Set up Uptime Robot

- Go to [https://uptimerobot.com](https://uptimerobot.com)
- Create a new monitor (HTTP/S type)
- Enter your Render URL (e.g., `https://your-bot.onrender.com`)
- Set the interval to 5 minutes

## Server Configuration

Make sure your server includes the following:

- A role named `comrade` (or your preferred post-verification role)
- A role named `unverified`
- A text channel named `welcome`
- A text channel named `user-answers` under a category called `admin & rules`
- Verification command allowed **only** in `start-here-for-verification` or `polls-and-tests`

These names are matched exactly, so check spelling and capitalization.

## File Structure

```
discord-verification-bot/
├── main.py             # Starts the bot and handles startup
├── handlers.py         # Quiz and role management logic
├── quiz.py             # Loads and shuffles quiz data
├── utils.py            # Helper functions for retry tracking and messages
├── quiz.json           # Full quiz content
├── messages.json       # Welcome messages
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.