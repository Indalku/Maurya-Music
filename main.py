import asyncio
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION

# Main Bot Client
bot = Client(
    "MauryaMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

# Assistant Account Client (Jo Voice Chat join karega)
assistant = Client(
    "MauryaAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call_py = PyTgCalls(assistant)

async def start_bot():
    print("🚀 Maurya Music Bot start ho raha hai...")
    await bot.start()
    await assistant.start()
    await call_py.start()
    print("✅ Maurya Music Bot aur Assistant dono online hain!")
    await idle()
    await bot.stop()
    await assistant.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
