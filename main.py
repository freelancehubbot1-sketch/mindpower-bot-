import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("ОШИБКА: Задай TELEGRAM_BOT_TOKEN и GEMINI_API_KEY в панели Render -> Environment!")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот MindPower на базе Google Gemini. Напиши мне что-нибудь!")

@dp.message()
async def chat_handler(message: types.Message):
    user_text = message.text or message.caption or "Опиши это"
    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Произошла ошибка при обращении к ИИ: {e}")

async def main():
    print("Бот MindPower успешно запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
