import asyncio
from aiogram import Bot, Dispatcher, types
from datetime import date

import sqlite3

import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv("BOT_KEY")

bot = Bot(token=bot_key)
dp = Dispatcher()

db = sqlite3.connect('database.db')
cursor = db.cursor()


@dp.message(lambda message:  message.text and message.text.lower()[:7] == 'решение')
async def add_base(message: types.Message):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {message.from_user.username} (username, decision, date)")
    decision = cursor.execute(f"SELECT * FROM {message.from_user.username} WHERE username = ? and decision = ?", (message.from_user.username, message.text[8:],)).fetchall()
    if not decision:
        cursor.execute(f"INSERT INTO {message.from_user.username} VALUES (?, ?, ?)", (message.from_user.username, message.text[8:], date.today().strftime("%d/%m/%y")))
        db.commit()
    print(decision)

@dp.message(lambda message: message.text and message.text.lower()[:20] == 'показать все решения')
async def show_decision(message: types.Message):
    decisions = cursor.execute(f"SELECT * FROM {message.text[31:]}  WHERE date = ? and username = ?", (message.text[21:29], message.text[31:])).fetchall()
    db.commit()

    count = 0
    answer = ''

    for item in decisions:
        answer += f'{count + 1})  пользователь: @{item[0]}\n    решение: {item[1]}\n    дата: {item[2]}\n\n'
        count += 1

    if decisions:
        await message.answer(answer)
    else:
        await message.answer("решений нет")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())

