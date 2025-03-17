import json, gettext, sys
from os import path
from gettext import NullTranslations

# from main import ROOT_DIR

def get_project_root():
    """
    Возвращает путь до корня проекта на основе sys.path.
    """
    for file_path in sys.path:
        if path.exists(path.join(file_path, 'main.py')):
            return file_path
    raise FileNotFoundError("Корень проекта не найден.")

def save_conversation(conversation, filename='conversation.txt'):
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            for line in conversation:
                file.write(line)
    except IOError as err:
        print(_('Ошибка при сохранении файла:'), err)

def load_conversation(filename='conversation.txt'):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(_('Файл c историей общения не найден.'))
        return []



class ChatConfig:
    DEFAULT_CONFIG = {
        "language": "russian",
        "user_name": "Гость"
    }

    def __init__(self, language_pack):
        self.current_config = {}
        self.load()
        self.ru_language, self.en_language = language_pack


        match self.current_config['language']:
            case 'russian':
                self.ru_language.install()
            case 'english':
                self.en_language.install(['en'])
            # case _: self.ru_language.install()

        # translation.install()


    def save(self, filename='config.json'):
        try:
            with open(filename, 'w') as file:
                file.write(json.dumps(self.current_config))
        except IOError as err:
            print(_('Ошибка при сохранении файла:'), err)

    def load(self, filename='config.json'):
        try:
            with open(filename, 'r') as file:
                self.current_config = json.loads(file.read())
                print(self.current_config)
        except FileNotFoundError:
            self.current_config = self.DEFAULT_CONFIG
            self.save()

    def change(self, param_name, param_value):
        self.current_config[param_name] = param_value
        self.save()

    def get_conf_as_string(self):
        return _('Выбран язык: %s, Ваше имя: %s') % (
            self.current_config['language'],
            self.current_config['user_name'])

    def chenge_language(self, message):
        if _('англиский') in message.lower():
            self.change(param_name='language', param_value='english')
            self.en_language.install()
            print('English is set')
        elif _('русский') in message.lower():
            self.change(param_name='language', param_value='russian')
            self.ru_language.install()
            print('Установлен Русский язык')
        else:
            return _('Список доступных языков: Русский и Англиский')
        return self.get_conf_as_string()
