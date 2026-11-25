# 🎵 Maurya Music Bot

Telegram Group Voice Chat me gaane bajane wala ek fast aur lightweight Music Bot (Pyrogram + PyTgCalls).

## ✨ Features
- `/play <song name>` - YouTube se gaana search karke Voice Chat me bajaye
- `/pause` - Chal rahe gaane ko pause kare
- `/resume` - Paused gaane ko wapas chalaye
- `/skip` - Current gaane ko skip karke agla gaana chalaye
- `/stop` - Gaana band kare aur Voice Chat leave kare

## ⚙️ Setup & Deployment
1. `.env.example` ko rename karke `.env` banayein (ya Render/VPS ke Environment Variables me values dalein):
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `STRING_SESSION`
   - `OWNER_ID`
2. Server par FFmpeg install hona zaroori hai (Docker use karne par auto-install ho jayega).
3. Run karein: `python3 main.py`
