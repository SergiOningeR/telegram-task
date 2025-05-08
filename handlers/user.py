from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.models import create_task, get_user_tasks
from loader import dp
from aiogram.dispatcher.filters import Command

class TaskState(StatesGroup):
    title = State()
    comment = State()
    phone = State()
    urgency = State()
    photo = State()

@dp.message_handler(Command("start"))
async def start(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Создать задачу", "Просмотреть мои задачи", "Удалить задачу")
    await msg.answer("Привет! Я бот для технических заявок.", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text == "Создать задачу")
async def new_task(msg: types.Message):
    await msg.answer("Введите название задачи:")
    await TaskState.title.set()

@dp.message_handler(state=TaskState.title)
async def get_title(msg: types.Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer("Введите комментарий:")
    await TaskState.comment.set()

@dp.message_handler(state=TaskState.comment)
async def get_comment(msg: types.Message, state: FSMContext):
    await state.update_data(comment=msg.text)
    await msg.answer("Введите номер телефона:")
    await TaskState.phone.set()

@dp.message_handler(state=TaskState.phone)
async def get_phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    kb = InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("Низкая", callback_data="urg_low"),
        InlineKeyboardButton("Средняя", callback_data="urg_medium"),
        InlineKeyboardButton("Важная", callback_data="urg_high")
    )
    await msg.answer("Выберите срочность задачи:", reply_markup=kb)
    await TaskState.urgency.set()

@dp.callback_query_handler(lambda c: c.data.startswith("urg_"), state=TaskState.urgency)
async def get_urgency(callback: types.CallbackQuery, state: FSMContext):
    urgency_map = {"urg_low": "Низкая", "urg_medium": "Средняя", "urg_high": "Важная"}
    urgency = urgency_map[callback.data]
    await state.update_data(urgency=urgency)
    await callback.message.answer("Прикрепите изображение (по желанию) или нажмите /skip, чтобы пропустить.")
    await TaskState.photo.set()

@dp.message_handler(commands=["skip"], state=TaskState.photo)
async def skip_photo(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = create_task(
        data["title"], data["comment"], data["phone"], data["urgency"],
        msg.from_user.id, msg.from_user.full_name
    )
    await msg.answer(f"Задача #{task_id} создана!")
    await state.finish()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=TaskState.photo)
async def get_photo(msg: types.Message, state: FSMContext):
    photo_id = msg.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    data = await state.get_data()
    task_id = create_task(
        data["title"], data["comment"], data["phone"], data["urgency"],
        msg.from_user.id, msg.from_user.full_name,
        photo_id=photo_id
    )
    await msg.answer(f"Задача #{task_id} создана!")
    await state.finish()

@dp.message_handler(lambda msg: msg.text == "Просмотреть мои задачи")
async def view_tasks(msg: types.Message):
    tasks = get_user_tasks(msg.from_user.id)
    if not tasks:
        await msg.answer("У вас нет задач.")
        return
    for task in tasks:
        text = f"📌 Задача #{task['id']}
Название: {task['title']}
Комментарий: {task['comment']}
Телефон: {task['phone']}
Срочность: {task['urgency']}
Статус: {task['status']}"
        await msg.answer(text)