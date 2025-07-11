# Discord Verification Bot

This is a Python-based Discord bot designed to automate user verification through a custom quiz system. It ensures that new members meet a specific level of familiarity with server expectations before being granted full access.

## Features

- **DM-based quiz delivery**  
  Users initiate the quiz by typing `!verifyme`. The bot sends a private 8-question multiple-choice quiz directly to their DMs.

- **Shuffled question order**  
  Each session presents the quiz in a randomized order to reduce predictability.

- **Automated scoring**  
  Each response is scored instantly. A total of 40 points is possible, with a passing score set at 30.

- **Role assignment**  
  Upon passing, the bot assigns a designated role (e.g., `comrade`) and removes the `unverified` role automatically.

- **Personalized welcome**  
  One of five randomized welcome messages is posted in the `#welcome` channel when someone verifies successfully.

- **Answer logging**  
  All user responses and scores are sent to a private `#user-answers` channel within the `admin & rules` category for moderation and transparency.

- **Graceful failure handling**  
  If a user has DMs disabled or the session times out, the bot notifies them with friendly and helpful messages.

## Hosting & Uptime

The bot runs as an **active web service on [Render](https://render.com)** and is kept alive by periodic HTTP pings from [Uptime Robot](https://uptimerobot.com). A lightweight Flask app is used to serve a basic endpoint that UptimeRobot can monitor, preventing the bot from going idle due to inactivity.

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

Create a `.env` file (or configure your variables in Render) with:

```
DISCORD_TOKEN=your-bot-token-here
```

### 4. Deploy to Render

- Create a **Web Service** in your Render dashboard.
- Use `python your_script.py` as the start command.
- Set `DISCORD_TOKEN` in your Render environment variables.
- Render will assign a public URL that UptimeRobot can ping.

### 5. Set up Uptime Robot

- Go to [uptimerobot.com](https://uptimerobot.com)
- Add a new HTTP(s) monitor
- Paste your Render URL (e.g. `https://your-bot.onrender.com`)
- Set check interval to every 5 minutes

## Server Configuration

To ensure the bot functions as expected, make sure your server has:

- A role named `comrade`
- A role named `unverified`
- A text channel named `welcome`
- A text channel named `user-answers` nested under a category named `admin & rules`

These names are matched exactly, so double-check spelling and capitalization.

## File Structure

```
discord-verification-bot/
├── main.py               # Main bot script with quiz logic
├── requirements.txt      # Python dependencies
└── README.md             # Project overview and instructions
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
