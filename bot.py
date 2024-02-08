import asyncio 
from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,ReplyKeyboardRemove,Message,CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from decouple import config

from texts.text import reg_text
from states import UserState

async def write_user_register(data):
    with open('users.txt', 'w') as file:
        file.write(data)
    pass

TOKEN = config('TOKEN')

bot = Bot(TOKEN)

dp = Dispatcher()

start_inline_kb = InlineKeyboardBuilder(
    markup=[
        [
        InlineKeyboardButton(text = 'Регистрация',callback_data='register')
        ]
    ]
)
del_kb = ReplyKeyboardRemove()


@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Приветствую тебя в нашем боте",
        reply_markup=start_inline_kb.as_markup(),
    )

@dp.callback_query(lambda query: query.data == 'register')
async def register_user(query: CallbackQuery, state: FSMContext)-> None:
    await state.set_state(UserState.phone_number)
    await query.message.answer(text = 'Введите телефонный номер:')
        
@dp.message(UserState.phone_number)
async def set_phone_number(message: Message,state: FSMContext)-> None:
    await state.update_data(phone_number=message.text)
    await state.set_state(UserState.FIO)
    await message.answer(f'Введите ФИО')

@dp.message(UserState.FIO)
async def set_fio(message: Message,state: FSMContext)-> None:
    data = await state.update_data(FIO=message.text)
    await state.clear()
    await message.answer('Вы успешно зарегались...ждите')
    await sucessful_register(message=message, data=data)


async def sucessful_register(message: Message, data: Dict[str, Any])-> None:
    text = f"Вы успешно зарегистрировались {data}"
    await write_user_register(str(data))
    await message.answer(text = text)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())