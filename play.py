import asyncio
from collections import deque
from pyrogram import Client, filters
from pytgcalls.types import MediaStream
import yt_dlp
from main import call_py

# Har group ke liye alag song queue
queues = {}

def get_audio_info(query: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "default_search": "ytsearch1"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]
        return info["url"], info["title"]

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await message.reply(
        "🎵 **Welcome to Maurya Music Bot!**\n\n"
        "Mujhe apne Telegram Group me add karein, Admin banayein (Manage Voice Chats permission ke sath), "
        "aur `/play <gaane ka naam>` bhej kar gaana bajayein!"
    )

@Client.on_message(filters.command("play") & filters.group)
async def play_song(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Kripya gaane ka naam likhein. Example: `/play Kesariya`")

    chat_id = message.chat.id
    query = message.text.split(None, 1)[1]
    msg = await message.reply("🔎 Gaana search kiya ja raha hai...")

    try:
        loop = asyncio.get_event_loop()
        audio_url, title = await loop.run_in_executor(None, get_audio_info, query)

        if chat_id not in queues:
            queues[chat_id] = deque()

        if len(queues[chat_id]) == 0:
            queues[chat_id].append((audio_url, title))
            await call_py.play(chat_id, MediaStream(audio_url))
            await msg.edit(f"🎶 **Ab baj raha hai:** {title}")
        else:
            queues[chat_id].append((audio_url, title))
            await msg.edit(f"➕ **Queue me joda gaya (#{len(queues[chat_id])}):** {title}")
    except Exception as e:
        await msg.edit(f"⚠️ Error aaya: `{e}`")

@Client.on_message(filters.command("pause") & filters.group)
async def pause_song(client, message):
    try:
        await call_py.pause_stream(message.chat.id)
        await message.reply("⏸️ Gaana pause kar diya gaya hai.")
    except Exception as e:
        await message.reply(f"⚠️ Error: `{e}`")

@Client.on_message(filters.command("resume") & filters.group)
async def resume_song(client, message):
    try:
        await call_py.resume_stream(message.chat.id)
        await message.reply("▶️ Gaana wapas chalu kar diya gaya hai.")
    except Exception as e:
        await message.reply(f"⚠️ Error: `{e}`")

@Client.on_message(filters.command("skip") & filters.group)
async def skip_song(client, message):
    chat_id = message.chat.id
    if chat_id in queues and len(queues[chat_id]) > 1:
        queues[chat_id].popleft()
        next_url, next_title = queues[chat_id][0]
        await call_py.play(chat_id, MediaStream(next_url))
        await message.reply(f"⏭️ Skip kiya gaya! **Ab baj raha hai:** {next_title}")
    else:
        queues.pop(chat_id, None)
        try:
            await call_py.leave_call(chat_id)
        except Exception:
            pass
        await message.reply("⏹️ Queue me koi aur gaana nahi hai, Voice Chat leave kar diya gaya.")

@Client.on_message(filters.command("stop") & filters.group)
async def stop_song(client, message):
    chat_id = message.chat.id
    queues.pop(chat_id, None)
    try:
        await call_py.leave_call(chat_id)
        await message.reply("⏹️ Music band kar diya gaya hai aur Voice Chat leave kar diya.")
    except Exception as e:
        await message.reply(f"⚠️ Error: `{e}`")
