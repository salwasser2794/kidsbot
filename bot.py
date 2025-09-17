import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📊 Курсы"))
main_menu.add(KeyboardButton("📰 Новости"))
main_menu.add(KeyboardButton("❓ FAQ"))
main_menu.add(KeyboardButton("📞 Поддержка"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Привет! Я информационный бот биржи Traiex.\nВыбери раздел в меню ниже 👇",
        reply_markup=main_menu
    )

@dp.message_handler(lambda message: message.text == "📊 Курсы")
async def rates(message: types.Message):
    await message.answer("📊 Текущие курсы Traiex:\nBTC/USDT: 65,000 $\nETH/USDT: 3,500 $")

@dp.message_handler(lambda message: message.text == "📰 Новости")
async def news(message: types.Message):
    await message.answer("📰 Последние новости Traiex:\n- Новая акция для трейдеров!\n- Снижение комиссий до 0.1%.")

@dp.message_handler(lambda message: message.text == "❓ FAQ")
async def faq(message: types.Message):
    await message.answer("❓ FAQ:\n1. Как зарегистрироваться?\n2. Как пополнить счёт?\n3. Поддержка")

@dp.message_handler(lambda message: message.text == "📞 Поддержка")
async def support(message: types.Message):
    await message.answer("📞 Связаться с поддержкой: support@traiex.com\nTelegram: @TraiexSupport")

@dp.message_handler()
async def fallback(message: types.Message):
    await message.answer("🤔 Я тебя не понял. Выбери раздел в меню 👇", reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
