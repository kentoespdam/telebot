import importer_test
import telegram
from config import TELEGRAM_GROUP_ID, TELEGRAM_TOKEN
import asyncio


async def main():
    bot = telegram.Bot(TELEGRAM_TOKEN)
    async with bot:
        await bot.send_message(chat_id=TELEGRAM_GROUP_ID, text="Hello World")

if __name__ == "__main__":
    asyncio.run(main())
