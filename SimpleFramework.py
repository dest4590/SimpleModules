# Помощник для моих модулей
from telebot import types

# Жирный текст
bold = lambda text: '<b>' + text + '</b>'

# Моно текст
mono = lambda text: '<code>' + text + '</code>'

# Получить аргументы из сообщения
def getArgs(message: types.Message):
    return message.text.split(' ')[1:]

# Проверить аргументы, ли они вообще есть
def checkArgs(message: types.Message, index: int):
    try:
        getArgs(message)[index]
        return True
    except IndexError:
        return False