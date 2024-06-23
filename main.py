import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def correct_text(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that corrects text."},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Error during OpenAI API call: {e}")
        return "Произошла ошибка при обработке текста."

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне текст, и я постараюсь его корректировать с помощью ChatGPT.")

@dp.message_handler()
async def handle_text(message: types.Message):
    corrected_text = await correct_text(message.text)
    await message.reply(corrected_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
