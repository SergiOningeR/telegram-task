from aiogram import types
from app.database import get_connection
from loader import dp

@dp.callback_query_handler(lambda c: c.data.startswith("task_action:"))
async def task_actions(callback: types.CallbackQuery):
    action, task_id = callback.data.split(":")[1:]
    conn = get_connection()
    cursor = conn.cursor()

    if action == "take":
        cursor.execute("UPDATE tasks SET status = 'выполняется' WHERE id = ?", (task_id,))
        conn.commit()
        await callback.message.answer(f"Задача #{task_id} взята в работу.")
    elif action == "cancel":
        cursor.execute("UPDATE tasks SET status = 'отменена' WHERE id = ?", (task_id,))
        conn.commit()
        await callback.message.answer(f"Задача #{task_id} отменена.")
    elif action == "done":
        cursor.execute("UPDATE tasks SET status = 'закрыта' WHERE id = ?", (task_id,))
        conn.commit()
        await callback.message.answer(f"Задача #{task_id} закрыта.")
    conn.close()