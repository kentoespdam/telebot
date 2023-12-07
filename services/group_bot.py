import telegram

from config import TELEGRAM_GROUP_ID, TELEGRAM_TOKEN


async def send_to_group(message: str) -> None:
    print(f"message: {message}")
    bot = telegram.Bot(TELEGRAM_TOKEN)
    async with bot:
        await bot.send_message(
            chat_id=TELEGRAM_GROUP_ID,
            text=message,
            parse_mode="Markdown"
        )
