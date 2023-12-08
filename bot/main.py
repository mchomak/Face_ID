import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F, MagicFilter
from aiogram.filters import Command
from aiogram.types import FSInputFile, ReplyKeyboardRemove, BotCommand

import Get_encodings, video2photos
from config import Path

from bot_config import BOT_TOKEN
from db_functions import *
from functions import *
from keyboards import *
from messages import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(text=start_text)
    await message.answer(text=what_way, reply_markup=start_kb)


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(list_cmds)


@dp.message(F.text == "Face ID")
async def face_id(message: types.Message):
    await message.delete()
    await message.answer("Введите своё ФИО", reply_markup=ReplyKeyboardRemove())


@dp.message(F.text == "Пропуск")
async def let_pass(message: types.Message):
    await message.delete()
    await message.answer("У вас уже есть обычный пропуск", reply_markup=ReplyKeyboardRemove())
    await smth_else(message)


@dp.message(F.text == "Отмена")
async def cancel(message: types.Message):
    await message.delete()
    await message.answer("Напиши /start, если передумаете", reply_markup=ReplyKeyboardRemove())
    await smth_else(message)


@dp.message(F.text == "Нет")
async def smth_else(message: types.Message):
    await message.answer("Что-то ещё?\n(напишите /help, чтобы увидеть все доступные команды)",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Хорошего дня")


@dp.message(MagicFilter.len(F.text.split()) >= 3)
async def name_handler(message: types.Message):
    name = message.text
    user_id = message.from_user.id
    en_name = translate(*name.split()[:2])
    if check_name(en_name, user_id):
        await want_to_update(message)
    else:
        make_dirs(en_name)
        await start_register(message)


async def want_to_update(message: types.Message):
    await message.answer(wanna_update, reply_markup=yes_no_kb)


@dp.message(F.text == "Да")
async def update_data(message: types.Message):
    await message.delete()
    # photo = get_photo(message.from_user.id)
    # img = FSInputFile(photo)
    # await message.answer_photo(img, caption="Ваше фото сейчас")
    await message.answer("Что вы хотите сделать в вашими данными?", reply_markup=del_ch_save_kb)


@dp.message(F.text == 'Удалить')
async def delete_data(message: types.Message):
    await message.delete()
    res = delete_dirs(message.from_user.id)
    if res:
        await message.answer("Ваши данные удалены\n/start", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Что-то пошло не так...\n/start", reply_markup=ReplyKeyboardRemove())


@dp.message(F.text == 'Изменить')
async def edit_data(message: types.Message):
    await message.delete()
    delete_photo(message.from_user.id)
    await message.answer("Отправьте новое фото", reply_markup=ReplyKeyboardRemove())


@dp.message(F.text == "Сохранить")
async def save_data(message: types.Message):
    await message.delete()
    await message.answer("Данные сохранены!\n/start", reply_markup=ReplyKeyboardRemove())


async def start_register(message: types.Message):
    await message.answer(start_reg_text, reply_markup=accept_kb)


@dp.message(F.text == 'Даю согласие')
async def agree_register(message: types.Message):
    await message.delete()
    await message.answer("Отлично!\nС помощью чего вам будет удобнее настроить систему?", reply_markup=circle_photo_kb)


@dp.message(F.text == 'Не даю')
async def disagree(message: types.Message):
    await message.delete()
    await message.answer("К сожалению, мы не можем идти дальше без вашего согласия")
    await smth_else(message)


@dp.message(F.text == "Фотография (3-5)")
async def reg_photo(message: types.Message):
    await message.delete()
    await message.answer("Отправьте ваше фото", reply_markup=ReplyKeyboardRemove())


@dp.message(F.photo)
async def get_user_photo(message: types.Message):
    file = await bot.get_file(message.photo[-1].file_id)
    name = get_user_name(message.from_user.id)
    await bot.download_file(file.file_path, f'{Path["image"]}/{name}/image{get_num_photos(name)}.png')
    await message.answer("Фото сохранено", reply_markup=next_kb)


@dp.message(F.text == "Кружочек (рекомендуется)")
async def reg_circle_video(message: types.Message):
    await message.delete()
    await message.answer("Отправьте кружочек", reply_markup=ReplyKeyboardRemove())


@dp.message(F.video_note)
async def get_user_circle(message: types.Message):
    print('circle_ok')
    file_id = message.video_note.file_id
    file = await bot.get_file(file_id)
    user_id = message.from_user.id
    name = get_user_name(user_id)
    await bot.download_file(file.file_path, f'{Path["video"]}/{name}/video{get_num_videos(name) + 1}.avi')
    video2photos.main(name, Path['circle_image'])
    await message.answer("Кружочек сохранен", reply_markup=ReplyKeyboardRemove())
    await show_acc(message)


@dp.message(F.text == 'Дальше')
async def show_acc(message: types.Message):
    photo = get_photo(message.from_user.id)
    if photo:
        img = FSInputFile(photo)
        name = get_user_name(message.from_user.id)
        await message.answer_photo(img, caption=name)
    else:
        photo = get_circle_photo(message.from_user.id)
        photo = FSInputFile(photo)
        name = get_user_name(message.from_user.id)
        await message.answer_photo(photo=photo, caption=name)
    await message.answer("Всё верно?", reply_markup=yes_no_kb2)


@dp.message(F.text == "да")
async def process_reg(message: types.Message):
    await message.answer("Ваши файлы обрабатываются, пододжите немного...")
    name = get_user_name(message.from_user.id)
    if get_num_photos(name):
        mode = 'photo'
    elif get_num_videos(name):
        mode = 'video'
    Get_encodings.main(1, mode, name, name)
    await message.answer("Ваши данные успешно сохранены!", reply_markup=ReplyKeyboardRemove())
    delete_photo(message.from_user.id)
    await smth_else(message)


@dp.message(F.text == 'нет')
async def error_reg(message: types.Message):
    await message.delete()
    await message.answer(
        "К сожалению, при добавлении ваших данных произошла ошибка. Попробуйте ещё раз позже или свяжитесь со службой "
        "поддержки", reply_markup=ReplyKeyboardRemove())
    await smth_else(message)


async def set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь")
    ])


async def main():
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
