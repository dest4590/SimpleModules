# SA Module, by Purpl3 (https://t.me/PLNT_YT)
from telebot import types, TeleBot

# import SimpleFramework
try: 
    from SimpleFramework import *
except ImportError:
    print('SimpleFramework not found, SimpleAdmin may not work.')

cmds = []

class ACommand:
    def __init__(self, name: str, desc: str, params: list, access: str):
        self.name = name
        self.desc = desc
        self.params = params
        self.access = access

        cmds.append(self)

    def get(self):
        return self.__dict__

def setup(bot: TeleBot):
    print('SimpleAdmin initialized. Enjoy!') # омагад

    async def raiseError(message: types.Message, text: str):
        await bot.reply_to(message, '🚫 ' + bold(text))

    async def checkAdmin(message: types.Message):
        user = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if user.status == 'administrator' or user.status == 'creator':
            return True
        else: False

    ACommand('ahelp', 'Навигация по SimpleAdmin', ['command'], 'user')
    @bot.message_handler(commands=['ahelp'])
    async def ahelp(message: types.Message):
        if not checkArgs(message, 0):
            text = f'''{bold('🛠 Команды SimpleAdmin:')}'''

            for cmd in cmds:
                text += bold(f'''\n/{cmd.get()['name']} - {cmd.get()['desc']}''')

            await bot.reply_to(message, text)
        else:
            for cmd in cmds:
                if cmd.get()['name'] == getArgs(message)[0]:
                    cmdData = cmd.get()
                    text = bold(f'Команда: /' + cmdData['name'])

                    if len(cmdData['params']) != 0: 
                        text += bold('\nПараметры: ' + ' '.join(['(' + arg + ')' for arg in cmd.get()['params']]))

                    text += bold('\nОписание: ' + cmdData['desc'])
                    
                    if cmdData['access'] == 'admin' and await checkAdmin(message) == True: # если команда админская и у пользователя есть админка
                        text += bold('\n🔐 У вас есть доступ к этой команде')
                    
                    elif cmdData['access'] == 'admin' and not await checkAdmin(message) == False: # если у пользователя нету админки
                        text += bold('\n🚫 У вас нету доступа к этой команде')

                    try:
                        if getArgs(message)[1] == '-v': # если включен дебаг
                            text += f'\n🪲 {bold("Debug info:")}\n{bold("Dict: ")}' + f'''{mono(str(cmd.__dict__).replace('<', '{').replace('>', '}'))}\n{bold('Raw: ')}{mono(str(cmd).replace('<', '{').replace('>', '}'))}'''
                    
                    except IndexError: pass # пассать если не включен дебаг

                    await bot.reply_to(message, text)
                    
                    return # возращаем чтобы код дальше не шёл
                
            await raiseError(message, 'Команда не найдена!')

    
    ACommand('aban', 'Забанить пользователя', ['user'], 'admin')
    @bot.message_handler(commands=['aban'])
    async def ban(message: types.Message):
        if not await checkAdmin(message):
            await raiseError(message, 'У вас нет прав для выполнения этой команды!')
            return
        
        args = getArgs(message)
        if not checkArgs(message, 0): # Если админ не указал пользователя
            await raiseError(message, 'Укажите пользователя!')

        if args[0].isdigit():
            if int(args[0]) == message.from_user.id: # я себя захуя..
                await bot.send_photo(message.chat.id, 'https://i.imgur.com/DWScpZM.jpg', reply_to_message_id=message.id)
                return
                
            await bot.unban_chat_member(message.chat.id, args[0])
            await bot.reply_to(message, bold('✅ Пользователь заблокирован!'))

        else:
            await raiseError(message, 'Укажите айди пользователя!')
    
    ACommand('aunban', 'Разбанить пользователя', ['user'], 'admin')
    @bot.message_handler(commands=['aunban'])
    async def unban(message: types.Message):
        if not await checkAdmin(message):
            await raiseError(message, 'У вас нет прав для выполнения этой команды!')
            return
        
        args = getArgs(message)
        if not checkArgs(message, 0): # Если админ не указал пользователя
            await raiseError(message, 'Укажите пользователя!')
        
        if args[0].isdigit():
            await bot.unban_chat_member(message.chat.id, args[0])
            await bot.reply_to(message, bold('✅ Пользователь разблокирован!'))
        else:
            await raiseError(message, 'Укажите айди пользователя!')

    ACommand('ainfo', 'Информация об чате', [], 'user')
    @bot.message_handler(commands=['ainfo'])
    async def ainfo(message: types.Message):
        if message.chat.title != None: # чекать если есть инфа об чате
            membersCount = await bot.get_chat_member_count(message.chat.id)

            await bot.reply_to(message, bold(f'ℹ️ Информация об чате: {message.chat.title}\n') + 
f'''{bold('ℹ️ Айди: ')} {mono(str(message.chat.id))}
{bold('👥 Участники: ' + str(membersCount))}''') # это форматирование просто имба