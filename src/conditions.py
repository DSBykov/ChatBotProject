import nltk
from nltk import word_tokenize


def respond_to_greeting(message):
    greetings = [_('привет'), _('здравствуйте'), _('добрый день')]
    farewells = [_('пока'), _('до свидания'), _('прощай')]

    if any(list(map(lambda _: _ in message.lower(), greetings))):
        return _('И тебе привет!')
    elif message.lower() in farewells:
        return _('Пока! Хорошего дня!')
    else:
        return _('Я тебя не понимаю...')

def get_words_by_tag(msg: str, config):
    __tagged = get_tagget_message(msg, config)
    __result = []
    for w, t in __tagged:
        if (t == 'S') or (t == 'NNP'):
            __result.append(w)

    if len(__result) == 1:
        return __result[0]
    elif len(__result) > 1:
        return str.join(' ', __result) + '!'
    else:
        raise ValueError(_('Не удалось определить имя.'))
    # [('меня', 'S-PRO'), ('зовут', 'V'), ('Дмитрий', 'S'), ('Сергеевич', 'S')]

def get_tagget_message(row_string, config):
    parts = word_tokenize(text=row_string, language=config.current_config['language'])
    # filtered_sentence = [w for w in parts if not w.lower() in stop_words]
    print('filtered_sentence =', parts)
    tagged = nltk.pos_tag(parts, lang=config.current_config['language'][:3])
    print('tagged =', tagged)
    return tagged

def get_parts_message(row_string, config):
    parts = word_tokenize(text=row_string, language=config.current_config['language'])
    # filtered_sentence = [w for w in parts if not w.lower() in stop_words]
    print('filtered_sentence =', parts)
    return parts