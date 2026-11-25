# Indal Music Bot - Starter

Starter project for a Telegram group voice-chat bot.

## Included
- /start and /help
- /play plays one local audio file
- /pause, /resume and /stop

## Important limitations
- This is a starter, not a guaranteed production-ready deployment.
- Render Free services may sleep after inactivity; reliable 24/7 playback is not guaranteed.
- A Telegram group voice chat must already be active. The assistant account must be in the group and allowed to speak.
- Put an audio file you own or are licensed to stream at `audio/sample.mp3`.
- No YouTube/Spotify ripping or copyrighted-music downloading is included.
- Native `ntgcalls` compatibility depends on the host. Use a supported Linux host and Python 3.11 or 3.12 if installation fails.
- Never commit secrets or session strings to GitHub.

## Render
Build command: `pip install -r requirements.txt`
Start command: `python main.py`

Set these Render Environment variables: `BOT_TOKEN`, `API_ID`, `API_HASH`, `SESSION_STRING`, `DEFAULT_AUDIO`.

Get API credentials from https://my.telegram.org. Generate the Telethon StringSession only in a trusted environment; treat it like a password.
