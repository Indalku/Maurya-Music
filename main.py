
import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "🎵 Indal Music Bot चालू है!\n"
        "हमारा Music Bot तैयार हो रहा है।"
    )


async def health(request):
    return web.Response(text="Indal Music Bot is running!")


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable missing!")

    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    bot = Bot(token=BOT_TOKEN)

    print("Indal Music Bot started!")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
