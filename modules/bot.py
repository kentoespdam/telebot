import telegram

from dotenv import load_dotenv
import os

load_dotenv()


async def send_to_group(message):
    bot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))
    async with bot:
        await bot.send_message(
            chat_id=os.getenv("TELEGRAM_GROUP_ID"), 
            text=message, 
            parse_mode="Markdown")

# if __name__ == '__main__':
#     asyncio.run(send_to_group("Hello World"))
