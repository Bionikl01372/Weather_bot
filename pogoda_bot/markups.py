from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#кнопка главное меню
btnMain = KeyboardButton('Меню')


#Menu
start_cmd = KeyboardButton('/start')
bot_info = KeyboardButton('О боте')
help_btn = KeyboardButton('Помогите!')



mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(start_cmd, bot_info, help_btn)
menuGL = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnMain)




bot_cmd = KeyboardButton('/bot')

Main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(start_cmd, bot_cmd)