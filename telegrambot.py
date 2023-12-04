import asyncio
import telegram
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")


async def main():
    bot = telegram.Bot(token)
    async with bot:
        print((await bot.get_updates())[0])

if __name__ == '__main__':
    asyncio.run(main())