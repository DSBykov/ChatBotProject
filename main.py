# from numpy.f2py.symbolic import Language
import gettext
from src.conditions import respond_to_greeting
from src.functions import chat_bot
from src.file_operation import load_conversation, save_conversation, ChatConfig, get_project_root
from os import path

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords


# nltk.download('punkt_tab')
# nltk.download('popular')
# LANGUAGE = 'russian'
# stop_words = set(stopwords.words(LANGUAGE))

ROOT_DIR = path.dirname(__file__)

locale_dir = path.join(get_project_root(), 'locales')
print('locale_dir = ', locale_dir)
gettext.bindtextdomain(domain='messages', localedir=locale_dir)
ru_language = gettext.NullTranslations()
# locale_dir = path.join(path.dirname(__file__), 'locales')
en_language = gettext.translation(domain='messages', localedir=locale_dir, languages=['en'])

configuration = ChatConfig((ru_language, en_language))

print(_('Чат-бот: Привет! Добро пожаловать в чат-бот!'))

conversation = load_conversation()

# nltk.download('punkt_tab')
# nltk.download('popular')
# LANGUAGE = 'russian'
# nltk.download(f'averaged_perceptron_tagger_{configuration.current_config['language'][:3]}')
# nltk.download('averaged_perceptron_tagger_eng')

while True:
    user_input = input(_('Вы: '))

    if user_input.lower() == _('выход'):
        print(_('Чат-бот: До свидания!'))
        save_conversation(conversation)
        break

    # word_tokens = word_tokenize(text=user_input, language=LANGUAGE)
    # print(word_tokens)
    # filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # print(filtered_sentence)

    greetings_response = respond_to_greeting(user_input)
    if greetings_response != _('Я тебя не понимаю...'):
        response = _('Чат-Бот: %s') % greetings_response
    else:
        response = chat_bot(user_input, configuration)

    conversation.append(f'{configuration.current_config['user_name']}: {user_input}')
    conversation.append(response)
    print(response)