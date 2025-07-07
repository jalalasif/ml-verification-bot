# ml-verification-bot
Discord Verification bot.

# Marxist-Leninist Discord Verification Bot

This is a Discord bot that automates political vetting for new users joining a Marxist-Leninist-oriented server. Users are required to complete a quiz via direct message, answering 8 multiple-choice questions. The bot scores their responses, and if they pass the threshold (30/40), they are automatically assigned the **comrade** role on the server.

This bot is designed to deter liberal, reactionary, or fascist infiltration by filtering participants through questions rooted in Marxist-Leninist theory.

---

## 🔧 Features

- Sends users an automated DM when they run `!verifyme`
- Asks 8 political-theoretical questions (max 5 points per question)
- Accepts responses in A/B/C/D format (case-insensitive)
- Tallies score and grants access if score ≥ 30
- Automatically assigns the `comrade` role to verified users
- Provides feedback on score and whether they passed or failed
- Built in Python using `discord.py`

---

## 💡 How It Works

1. A new user joins the server and types `!verifyme` in the `#verification` channel.
2. The bot DMs them a series of 8 questions, one at a time.
3. Each answer is scored (some answers award fewer points; reactionary ones may score zero or negative).
4. If the user scores at least 30/40, they receive the `comrade` role automatically.
5. If not, they are encouraged to study and try again.

This ensures that users entering the space either already align with Marxist-Leninist principles or are sincerely open to learning them.

---

## 🚀 Deployment (Render)

This bot is designed to be hosted 24/7 on [Render.com](https://render.com) using a **Background Worker** process.

### 🔄 Setup Steps:

1. **Fork or clone this repo**, or upload it to your own GitHub account.
2. Create a **new Background Worker** on Render.
3. Connect your GitHub and select this repository.
4. In the Render setup:
   - **Runtime**: Python 3.11+
   - **Build Command**:  
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:  
     ```bash
     python main.py
     ```
5. Under **Environment Variables**, add:
   - `DISCORD_TOKEN` = *your bot token here*
6. Click **Deploy**. Render will keep your bot alive automatically!

---

## 📜 Requirements

Be sure your `requirements.txt` contains the following:

You can generate this yourself with:

```bash
pip freeze > requirements.txt

---


🛠️ Customization
	•	You can adjust the quiz content in main.py by editing the quiz = [...] block.
	•	You can change the required passing score or role name as needed.
	•	To add more questions or categories (e.g. environmentalism, anti-colonialism), just add to the list.

⸻

🤝 Contributing

Feel free to fork and modify this bot for other political purposes, including:
	•	Vetting for anti-imperialist groups
	•	Historical education
	•	Mutual aid vetting
	•	Reading group filtering

Pull requests welcome!

⸻

⚠️ Caution

This bot is intended to provide light vetting based on political alignment. It should not be used to police or harass users, nor to gatekeep in bad faith. It is meant to create a safer space for principled organizing.

⸻

📢 License

This project is open-source and free to use under the MIT License.
