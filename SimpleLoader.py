# SA Module, by Purpl3 (https://t.me/PLNT_YT)
from telebot import types, TeleBot
from datetime import datetime
import requests
import os

# import SimpleFramework
try: 
    from SimpleFramework import *
except ImportError: # бро, установи симпл фраемворк
    print('SimpleFramework not found, SimpleLoader may not work.')

# Import pytube, if not exist install it
try:
    import pytube 
except ImportError: # установка пай-тюбика
    import pip
    pip.main(['install', 'pytube'])

def setup(bot: TeleBot):
    print('SimpleLoader initialized. Enjoy!') # богатый робукс

    async def raiseError(message: types.Message, text: str):
        await bot.reply_to(message, '🚫 ' + bold(text))

    @bot.message_handler(commands=['download'])
    async def download(message: types.Message): # скачивание видео
        if not checkArgs(message, 0): # если пользователь не указал видео
            await raiseError(message, 'Введите ссылку на ютуб видео')
            return
        
        args = getArgs(message) # получить аргументы команды

        # не бейте за `== True`, я для уверенности ((
        if args[0].startswith('https://youtube.com/') == True or args[0].startswith('https://www.youtube.com/') == True or args[0].startswith('https://youtu.be/') == True:
            try: # попробовать скачать видео
                video = pytube.YouTube(args[0]) # инфа об видео

                resolution_keyboard = types.InlineKeyboardMarkup()

                quality_in_keyboard = [] # список с доступным качеством для скачивания
                for stream in video.streams.filter(mime_type='video/mp4'):
                    if str(stream.resolution) in quality_in_keyboard:
                        pass

                    resolution_keyboard.add(types.InlineKeyboardButton('📹 MP4 ' + str(stream.resolution) + ' ' + str(stream.fps) + 'fps', callback_data='mp4@'+args[0]+'@'+str(stream.resolution))) # добавление кнопки
                    quality_in_keyboard.append(str(stream.resolution)) # добавление качества в список (чтобы не повторялось)

                audio = video.streams.filter(only_audio=True, mime_type='audio/mp4').desc().first() # брать лучший вариант скачивания аудио (чё я высрал)
                resolution_keyboard.add(types.InlineKeyboardButton('🎧 Audio ' + str(audio.abr), callback_data='audio@'+args[0]+'@'+str(audio.abr))) # добавить лучшее аудио

                await bot.send_message(message.chat.id, bold(f'Выберите качество: {str(video.title)}'), reply_markup=resolution_keyboard) # отправление сообщения с выбором качества

            except Exception as e:
                print(f'Video download error: {e}')
                await raiseError(message, 'Ошибка загрузки видео') # выдавать ошибку
        
        else:
            await raiseError(message, 'Введите ссылку на ютуб видео') # ну сказали же
            return

    @bot.callback_query_handler(func=lambda call: str(call.data).startswith('mp4') or str(call.data).startswith('audio')) # callback на клавиатуру выбора качества
    async def work_download(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id, 'Скачиваю...') # тяжело..
        # качаем
        video = pytube.YouTube(query.data.split('@')[1]) # инфо об видео

        if query.data.split('@')[0] == 'mp4': # если выбрано видео
            filename = 'temp' + str(datetime.now()) +'.mp4'
            video.streams.filter(file_extension='mp4', res=query.data.split('@')[2]).first().download('./', filename)

        elif query.data.split('@')[0] == 'audio': # если выбрано аудио
            filename = 'temp' + str(datetime.now()) +'.mp3'
            video.streams.filter(mime_type='audio/mp4', abr=query.data.split('@')[2], type='audio').first().download('./', filename)

        if query.data.split('@')[0] == 'mp4': # если выбрано видео
            # используем envs.sh, потому-что гуфи ахх телеграмм поддерживает файл не больше 20мб, а он аж целых 512 мегабайт!!!
            envs = requests.post('http://envs.sh', files={'file': open(filename, 'rb').read()}).content
            await bot.send_video(query.message.chat.id, envs.decode())
            
        elif query.data.split('@')[0] == 'audio': # если выбрано аудио
            await bot.send_audio(query.message.chat.id, open(filename, 'rb').read()) # ну тут простая отправка аудио, без envs.sh, потому-что аудио мало весит
       
        # удаляем файл чтобы место не бом бом
        os.remove(filename)