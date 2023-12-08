from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

kb = [
    [KeyboardButton(text="Face ID")],
    [KeyboardButton(text="Пропуск")],
    [KeyboardButton(text="Отмена")]
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите способ",
                               one_time_keyboard=True)

kb = [
    [KeyboardButton(text="Да")],
    [KeyboardButton(text="Нет")]
]

yes_no_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите способ",
                                one_time_keyboard=True)

kb = [
    [KeyboardButton(text="да")],
    [KeyboardButton(text="нет")]
]

yes_no_kb2 = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите способ",
                                 one_time_keyboard=True)

kb = [
    [KeyboardButton(text="Удалить")],
    [KeyboardButton(text="Изменить")],
    [KeyboardButton(text="Сохранить")]
]
del_ch_save_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите способ",
                                     one_time_keyboard=True)

kb = [
    [KeyboardButton(text="Даю согласие")],
    [KeyboardButton(text="Не даю")]
]

accept_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите способ",
                                one_time_keyboard=True)

kb = [
    [KeyboardButton(text="Кружочек (рекомендуется)")],
    [KeyboardButton(text="Фотография (3-5)")]
]

circle_photo_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите способ",
                                      one_time_keyboard=True)

kb = [
    [KeyboardButton(text='Дальше')]
]
next_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)