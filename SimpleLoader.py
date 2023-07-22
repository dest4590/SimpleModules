# SA Module, by Purpl3 (https://t.me/PLNT_YT)
from telebot import types, TeleBot
from datetime import datetime
import requests
import os

# import SimpleFramework
try: 
    from SimpleFramework import *
except ImportError:
    print('SimpleFramework not found, SimpleLoader may not work.')

# Import pytube, if not exist install it
try:
    import pytube
except ImportError:
    import pip
    pip.main(['install', 'pytube'])

def setup(bot: TeleBot):
    print('SimpleLoader initialized. Enjoy!')

    async def raiseError(message: types.Message, text: str):
        await bot.reply_to(message, '🚫 ' + bold(text))

    @bot.message_handler(commands=['download'])
    async def download(message: types.Message):
        if not checkArgs(message, 0):
            await raiseError(message, 'Введите ссылку на ютуб видео')
            return
        
        args = getArgs(message)

        if args[0].startswith('https://youtube.com/') == True or args[0].startswith('https://www.youtube.com/') == True or args[0].startswith('https://youtu.be/') == True:
            try:
                video = pytube.YouTube(args[0])

                resolution_keyboard = types.InlineKeyboardMarkup()

                quality_in_keyboard = []
                for stream in video.streams.filter(mime_type='video/mp4'):
                    if str(stream.resolution) in quality_in_keyboard:
                        pass
                    print(stream)
                    resolution_keyboard.add(types.InlineKeyboardButton('📹 MP4 ' + str(stream.resolution) + ' ' + str(stream.fps) + 'fps', callback_data='mp4@'+args[0]+'@'+str(stream.resolution)))
                    quality_in_keyboard.append(str(stream.resolution))

                audio = video.streams.filter(only_audio=True, mime_type='audio/mp4').desc().first()
                resolution_keyboard.add(types.InlineKeyboardButton('🎧 Audio ' + str(audio.abr), callback_data='audio@'+args[0]+'@'+str(audio.abr)))

                await bot.send_message(message.chat.id, bold(f'Выберите качество: {str(video.title)}'), reply_markup=resolution_keyboard)

            except Exception as e:
                await bot.send_message(message.chat.id, str(e))
                await raiseError(message, 'Ошибка загрузки видео')
        
        else:
            await raiseError(message, 'Введите ссылку на ютуб видео')
            return

    @bot.callback_query_handler(func=lambda call: str(call.data).startswith('mp4') or str(call.data).startswith('audio'))
    async def work_download(query: types.CallbackQuery):
        await bot.answer_callback_query(query.id, 'Скачиваю...')
        # качаем
        video = pytube.YouTube(query.data.split('@')[1])
        if query.data.split('@')[0] == 'mp4':
            filename = 'temp' + str(datetime.now()) +'.mp4'
            video.streams.filter(file_extension='mp4', res=query.data.split('@')[2]).first().download('./', filename)

        elif query.data.split('@')[0] == 'audio':
            filename = 'temp' + str(datetime.now()) +'.mp3'
            video.streams.filter(mime_type='audio/mp4', abr=query.data.split('@')[2], type='audio').first().download('./', filename)

        if query.data.split('@')[0] == 'mp4':
            envs = requests.post('http://envs.sh', files={'file': open(filename, 'rb').read()}).content
            await bot.send_video(query.message.chat.id, envs.decode())
            
        elif query.data.split('@')[0] == 'audio':
            await bot.send_audio(query.message.chat.id, open(filename, 'rb').read())
        
        # удаляем
        os.remove(filename)