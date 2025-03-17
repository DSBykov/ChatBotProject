import random, nltk
from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from math import sqrt
from src.conditions import get_words_by_tag

nltk.download('punkt_tab')
nltk.download('popular')
LANGUAGE = 'russian'
stop_words = set()
nltk.download('averaged_perceptron_tagger_rus')
nltk.download('averaged_perceptron_tagger_eng')


def chat_bot(message, config):
    PROMPT = _('Чат-бот: ')

    response_dict = {
        _('как дела'): _('У меня все хорошо, спасибо!'),
        _('что ты умеешь'): _('Я могу отвечать на простые вопросы.'),
        _('спасибо'): _('Всегда рад помочь :)'),
        _('включи музыку'): _('Кажется вы путаете меня с Алисой...')
    }
    random_responses = [
        _('Интересный вопрос!'),
        _('Я подумаю над этим.'),
        _('Давайте поговорим о чем-нибудь другом!?'),
        _('Спросите что нибудь попроще.')
    ]
    unknown_answer = _('Извините, я не знаю как ответить на это :(')

    math_operations = {
        _('плюс'): lambda x, y: x + y,
        '+': lambda x, y: x + y,
        _('минус'): lambda x, y: x - y,
        '-': lambda x, y: x - y,
        _('умножить'): lambda x, y: x * y,
        '*': lambda x, y: x * y,
        _('разделить'): lambda x, y: x / y if y != 0 else _('делить на 0 нельзя'),
        '/': lambda x, y: x / y if y != 0 else _('делить на 0 нельзя'),
        _('степени'): lambda x, y: x**y,
        _('корень'): lambda x, y: sqrt(y) if y >= 0 else _('Нельзя извлечь корень из отрицательного числа.')
    }

    if _('настройки') in message.lower():
        return config.get_conf_as_string()

    elif _('меня зовут') in message.lower():
        # parts = word_tokenize(text=message, language=LANGUAGE)
        # # filtered_sentence = [w for w in parts if not w.lower() in stop_words]
        # print('filtered_sentence =', parts)
        # tagged = nltk.pos_tag(parts, tagset='S', lang='rus')
        # print('tagged =', tagged)

        try:
            name = get_words_by_tag(message, config)
            config.change(param_name='user_name', param_value=name)
            return _('Приятно познакомится, %s') % config.current_config['user_name']
        except (IndexError, ValueError) as err:
            print(_('Возникла ошибка:'), err)
            return _('Я не рсслышал... Напишите: "Меня зовут <Ваше имя>"')

    elif _('изменить язык') in message.lower():
        return config.chenge_language(message)


    elif _('сколько будет') in message.lower():
        parts = word_tokenize(text=message, language=config.current_config['langu'])
        filtered_sentence = [w for w in parts if not w.lower() in stop_words]
        print('filtered_sentence =', filtered_sentence)

        try:
            if filtered_sentence[1] == _('корень'):
                num1 = None
                operation = filtered_sentence[1]
                num2 = int(filtered_sentence[2])
            else:
                num1 = int(filtered_sentence[2])
                operation = filtered_sentence[3]
                num2 = int(filtered_sentence[4])

            if operation in math_operations:
                return _('Результат: %s') % {math_operations[operation](num1, num2)}
        except (IndexError, ValueError) as err:
            print(_('Возникла ошибка:'), err)
            return _('Извините, я не могу обработать это выражение.')


    response = response_dict.get(message.lower(), unknown_answer)

    if response == unknown_answer:
        response = random.choice(random_responses)

    return PROMPT + response