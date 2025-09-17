import asyncio
import json
import random
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# === Загрузка профилей ===
with open("users.json", "r", encoding="utf-8") as f:
    users = json.load(f)

def save_users():
    """Сохраняем изменения в users.json (например, очки)"""
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_profile(user_id: int):
    """Получаем профиль по user_id"""
    return users.get(str(user_id))

def days_until(date_str: str) -> int:
    """Сколько дней до даты"""
    today = datetime.today().date()
    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    delta = (target - today).days
    return delta if delta >= 0 else (target.replace(year=today.year + 1) - today).days

# === Клавиатуры ===
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Игры и задания", callback_data="tasks")],
        [InlineKeyboardButton(text="📖 Интересный факт", callback_data="fact")],
        [InlineKeyboardButton(text="😂 Анекдот", callback_data="joke")],
        [InlineKeyboardButton(text="📅 Сколько дней до...", callback_data="days")],
        [InlineKeyboardButton(text="🏆 Мои очки", callback_data="points")],
        [InlineKeyboardButton(text="🙋 Кто я", callback_data="whoami")]
    ])

def days_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎂 День рождения Алисы", callback_data="days_alice")],
        [InlineKeyboardButton(text="🎂 День рождения Руслана", callback_data="days_ruslan")],
        [InlineKeyboardButton(text="🎄 Новый год", callback_data="days_newyear")],
        [InlineKeyboardButton(text="☀️ Каникулы", callback_data="days_holidays")]
    ])

# === Настройка бота ===
API_TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === Обработчики ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    profile = get_profile(message.from_user.id)
    if profile:
        await message.answer(
            f"{profile['greetings']}\nЧто хочешь сделать?",
            reply_markup=main_menu()
        )
    else:
        await message.answer("Привет! Тебя я пока не знаю 🤔")

# "Кто я"
@dp.callback_query(F.data == "whoami")
async def who_am_i(callback: types.CallbackQuery):
    profile = get_profile(callback.from_user.id)
    if profile:
        text = (
            f"Ты — {profile['name']} 🎉\n"
            f"📅 День рождения: {profile['birthday']}\n"
            f"🎯 Очков: {profile['points']}\n"
            f"💡 Например: {profile['facts'][0]}"
        )
        await callback.message.answer(text)
    await callback.answer()

# "Интересный факт"
@dp.callback_query(F.data == "fact")
async def fact(callback: types.CallbackQuery):
    profile = get_profile(callback.from_user.id)
    if profile:
        fact = random.choice(profile["facts"])
        await callback.message.answer(fact)
    await callback.answer()

# "Анекдот"
@dp.callback_query(F.data == "joke")
async def joke(callback: types.CallbackQuery):
    profile = get_profile(callback.from_user.id)
    if profile:
        joke = random.choice(profile["jokes"])
        await callback.message.answer(joke)
    await callback.answer()

# "Игры и задания"
@dp.callback_query(F.data == "tasks")
async def task(callback: types.CallbackQuery):
    profile = get_profile(callback.from_user.id)
    if profile:
        task = random.choice(profile["tasks"])
        await callback.message.answer(task)
        # начисляем очки
        profile["points"] += 1
        save_users()
        await callback.message.answer(f"Ты получил 1 очко! 🎯 Всего очков: {profile['points']}")
    await callback.answer()

# "Мои очки"
@dp.callback_query(F.data == "points")
async def points(callback: types.CallbackQuery):
    profile = get_profile(callback.from_user.id)
    if profile:
        await callback.message.answer(f"У тебя {profile['points']} очков 🎯")
    await callback.answer()

# "Сколько дней до..."
@dp.callback_query(F.data == "days")
async def days(callback: types.CallbackQuery):
    await callback.message.answer("Выбери событие:", reply_markup=days_menu())
    await callback.answer()

@dp.callback_query(F.data.startswith("days_"))
async def days_event(callback: types.CallbackQuery):
    data = callback.data

    if data == "days_alice":
        target = get_profile(123456789)["birthday"]
        text = f"До дня рождения Алисы 🎂 осталось {days_until(target)} дней!"
    elif data == "days_ruslan":
        target = get_profile(987654321)["birthday"]
        text = f"До дня рождения Руслана 🎂 осталось {days_until(target)} дней!"
    elif data == "days_newyear":
        target = users["common_dates"]["new_year"]
        text = f"До Нового года 🎄 осталось {days_until(target)} дней!"
    elif data == "days_holidays":
        target = users["common_dates"]["summer_holidays"]
        text = f"До летних каникул ☀️ осталось {days_until(target)} дней!"

    await callback.message.answer(text)
    await callback.answer()

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
