def main():
    import app.site_ver.functions as fun
    from random import randint
    import re

    task_name = 6
    task = 'Внимательно прочтите текст и исправьте ошибки в постановке мягких и твёрдых знаков.\n\n{}'

    def make_new_words(old_words):
        minipattern1 = re.compile('чн|чк|нч|нщ|рщ', re.IGNORECASE)
        minipattern2 = re.compile('(?:[бвгджзйклмнпрстфхцчшщ](?:ь|ъ)[еёюя])|(?:[жшщч](?:ъ|ь))', re.IGNORECASE)
        new_words = []

        for w in old_words:
            ind = True
            word = w[0]
            for m in re.finditer(minipattern1, w[0]):
                ct = randint(0, 1)
                if ind:
                    word = word[:m.start() + 1] + "ь" * ct + word[m.end() - 1:]
                    ind = False
            for m in re.finditer(minipattern2, word):
                a = randint(0, 2)
                if a == 0:
                    symbol = "ъ"
                elif a == 1:
                    symbol = "ь"
                else:
                    symbol = ""
                ct = randint(0, 1)
                if ind:
                    word = word[:m.start() + 1] + symbol * ct + word[m.end() - (m.end() - m.start() - 2):]
                    ind = False
            new_words.append(word)

        return new_words

    def make_key_words(old_words):
        key_words = []
        for w in old_words:
            s = w[0]
            minipattern2 = re.compile('(?:[бвгджзйклмнпрстфхцчшщ](?:ь|ъ)[еёюя])|(?:[жшщч](?:ъ|ь))', re.IGNORECASE)
            matches = re.finditer(minipattern2, s)
            for m in matches:
                symbol = "$"    #'ъ'
                if m[0][1].lower() == 'ь':
                    symbol = "@"
                s = s[:m.start() + 1] + symbol + s[m.end() - (m.end() - m.start() - 2):]
            s = s.replace('$', '[ъ]').replace('@', '[ь]')
            s = s.replace('чн', '[чн]').replace('чк', '[чк]').replace('нч', '[нч]').replace('нщ', '[нщ]').replace('рщ', '[рщ]')
            key_words.append(s)
        return key_words

    def make_text(new_words, old_words, text):
        L = len(text)
        l = len(text)
        for i, word in enumerate(old_words):
            text = text[:word.start() + l - L] + new_words[i] + text[word.end() + l - L:]
            if len(new_words[i]) != len(word[0]):
                l += len(new_words[i]) - len(word[0])
        text = text.replace('%^&.', '\n')
        return text

    text = fun.reading("6")
    sentences = fun.sts(text)

    #сочетания, в которых могут быть ъ/ь
    pattern = re.compile('\w+(?:(?:чн|чк|нч|нщ|рщ)|(?:[бвгджзйклмнпрстфхцчшщ](?:ь|ъ)[еёюя])|(?:[жшщч](?:ъ|ь)))\S+', re.IGNORECASE)

    task_sents, key_sents = [], []
    for sentence in sentences:
        old_words = pattern.finditer(sentence)
        new_words = make_new_words(pattern.finditer(sentence))
        key_words = make_key_words(pattern.finditer(sentence))
        '''print('new_words:', new_words)
        print('key_words:', key_words)
        print('old_words:', end = ' ')
        for w in old_words:
            print(w[0], end = ' ')
        print()'''

        new_text = make_text(new_words, old_words, sentence)

        task_sents.append(new_text)
        key_sents.append(key_words)
        #print(sentence)
        #print(new_text)
        #print(key_words)

    # форматируем тексты задания и ключей
    task_sents = ' '.join(task_sents)
    task_text = task.format(task_sents)

    key_text = task.format(key_sents)

    # записываем задание и ключи
    fun.writing(task_text, task_name)
    fun.writing_key(key_text, task_name)

    # выводим на сайт
    site_task_text = task_text.replace('\n', '<br>')
    print(site_task_text, "<br><br><br>")
    print("Ответы:<br>")
    site_key_text = key_text.replace('\n', '<br>')
    site_key_text = site_key_text.replace(task,'')
    print(site_key_text)

    show_task_name = str(task_name) +'_show'
    fun.writing(site_task_text,show_task_name )
