from aiogram import types
from loader import dp
from aiogram.dispatcher.filters import Command
import pandas as pd
from app.database import get_connection

@dp.message_handler(Command("export"))
async def export_tasks(msg: types.Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    if not rows:
        await msg.answer("Нет задач для экспорта.")
        return
    df = pd.DataFrame(rows, columns=rows[0].keys())
    df.to_csv("tasks_export.csv", index=False)
    with open("tasks_export.csv", "rb") as f:
        await msg.answer_document(types.InputFile(f, filename="tasks.csv"))