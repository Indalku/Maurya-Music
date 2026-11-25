import os
import asyncio
from aiohttp import web
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION

bot = Client(
    "MauryaMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")
)

assistant = Client(
    "MauryaAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call_py = PyTgCalls(assistant)

# Render Free Web Service ke liye dummy web server
async def handle(request):
    return web.Response(text="Maurya Music Bot is Running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def start_bot():
    print("🚀 Maurya Music Bot start ho raha hai...")
    await start_web_server()
    await bot.start()
    await assistant.start()
    await call_py.start()
    print("✅ Maurya Music Bot aur Assistant dono online hain!")
    await idle()
    await bot.stop()
    await assistant.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
