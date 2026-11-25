import asyncio, os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
SESSION_STRING = os.getenv('SESSION_STRING', '')
AUDIO_FILE = os.getenv('DEFAULT_AUDIO', 'audio/sample.mp3')
dp = Dispatcher()
calls = None

@dp.message(CommandStart())
async def start(message):
    await message.answer('🎵 Indal Music Bot online! Use /help for commands.')

@dp.message(Command('help'))
async def help_cmd(message):
    await message.answer('/play - play configured local audio\n/pause - pause\n/resume - resume\n/stop - stop\nOnly use audio you own or are licensed to stream.')

@dp.message(Command('play'))
async def play(message):
    if message.chat.type not in ('group', 'supergroup'):
        return await message.answer('Use /play in your group.')
    if not os.path.isfile(AUDIO_FILE):
        return await message.answer(f'Audio file not found: {AUDIO_FILE}')
    try:
        await calls.play(message.chat.id, MediaStream(AUDIO_FILE))
        await message.answer('▶️ Playing audio.')
    except Exception as exc:
        await message.answer(f'Playback failed: {type(exc).__name__}. Check active voice chat and assistant permissions.')

@dp.message(Command('pause'))
async def pause(message):
    try:
        await calls.pause(message.chat.id)
        await message.answer('⏸ Paused.')
    except Exception:
        await message.answer('Could not pause; is audio playing?')

@dp.message(Command('resume'))
async def resume(message):
    try:
        await calls.resume(message.chat.id)
        await message.answer('▶️ Resumed.')
    except Exception:
        await message.answer('Could not resume playback.')

@dp.message(Command('stop'))
async def stop(message):
    try:
        await calls.leave_call(message.chat.id)
        await message.answer('⏹ Stopped.')
    except Exception:
        await message.answer('No active playback found.')

async def main():
    global calls
    if not all([BOT_TOKEN, API_ID, API_HASH, SESSION_STRING]):
        raise RuntimeError('Set BOT_TOKEN, API_ID, API_HASH and SESSION_STRING in Render Environment.')
    app = web.Application()
    app.router.add_get('/', lambda req: web.Response(text='Indal Music Bot is running'))
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(app_runner_site := runner, '0.0.0.0', int(os.getenv('PORT', '10000'))).start()
    assistant = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await assistant.start()
    calls = PyTgCalls(assistant)
    await calls.start()
    bot = Bot(BOT_TOKEN)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await assistant.disconnect()
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
