# Installation script for modules
from configparser import ConfigParser
import os

def installModule(module: str):
    import pip
    pip.main(['install', module])

try:
    import wget
except ImportError:
    installModule('wget')

try:
    import rich
except ImportError:
    installModule('rich')

config = ConfigParser()
config.read('config')

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

modules = config.get('modules', 'Use').replace(' ', '').split(',')

print('Installed modules: ' + ', '.join(modules) + '\n')

modules_to_install = {
    'SimpleAdmin': 'Easy to use chat manager',
    'SimpleLoader': 'Fast youtube video downloader, with a choice of quality'
}

for module in modules:
    if module in modules_to_install.keys():
        print(module + ' already installed!')
        modules_to_install.pop(module)

if len(modules_to_install) == 0:
    print('All modules already installed!\nExiting..')
    quit()

skip = []

for m_key, m_value in zip(modules_to_install.keys(), modules_to_install.values()):
    while True:
        if len(modules_to_install) == 0:
            print('You installed all modules!')

        if m_key in skip:
            break

        clear()
        print(m_key + ': ' + m_value)
        choice = input('Install (y,n,q): ')
        if choice == 'y':
            current = config.get('modules', 'Use')
            if m_key in current:
                pass
            new = config.set('modules', 'Use', current + ', ' + m_key)
            config.write(open('config', 'w'))

            # Downloading module
            if not os.path.isdir('modules'):
                print('Modules folder not found, skipping downloading!\nPlease sure you moved this script to SimpleAI folder!')
            
            else:
                if not os.path.isfile('modules/' +  m_key + '.py'):
                    wget.download('https://raw.githubusercontent.com/dest4590/SimpleModules/main/' + m_key + '.py', 'modules/' + m_key + '.py')
                    print('\nDownloaded module!')

            input('Installed: ' + m_key + ' (press enter to continue) ')
            skip.append(m_key)

        elif choice == 'q':
            print('Exiting..')
            quit()

        elif choice == 'n':
            print('Skip module: ' + m_key + '!')
            skip.append(m_key)
        else:
            input('Choice, yes, no or quit!')
