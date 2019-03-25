def main(level):
    import app.site_ver.functions as fun
    import random

    task_name = 5
    task = 'В словах, заключенных в [квадратные скобки], буквы перепутаны местами. Восстановите правильный порядок.\n\n{}'

    def syllables(word, sn):
        vowels = 'уеыаоэяиюё'
        letters = 'йрлмн'
        stroka = word.text
        lemm = word.lem
        if (len([v for v in stroka if v in vowels]) > sn) and fun.check_min(lemm, level) and ('-' not in stroka):
            # берем те, в которых больше x слогов и есть в минимуме
            # print(word)
            n = 0
            sillabs = ''
            for i in range(len(stroka[::-1])):
                if stroka[i] in vowels:
                    sillabs += stroka[n:i] + stroka[i] + '-'
                    # print(sillabs)
                    n = i + 1
                    vowind = i
                else:
                    if i == len(stroka) - 1:
                        sillabs = sillabs[:-1] + stroka[n:] + '-'
            # выравнивание слогоделения для закрытых слогов в середине слова
            # print(sillabs)
            m = 0
            newsillabs = ''
            for j in range(len(sillabs)):
                if ((sillabs[j] in letters) and (sillabs[j - 1] == '-') and (sillabs[j + 1] not in vowels) and (
                        sillabs[j + 1] not in letters) and (sillabs[j + 1] != 'ь')):
                    newsillabs = newsillabs + sillabs[m:j - 1] + sillabs[j] + '-' + sillabs[j + 1:]
                    m = j + 1
                if (((sillabs[j] == 'ь') and (sillabs[j - 1] in letters)) and (sillabs[j - 2] == '-')):
                    newsillabs = newsillabs + sillabs[m:j - 2] + sillabs[j - 1:j + 1] + '-' + sillabs[j + 1:]
                    m = j + 1
            if newsillabs == '':
                newsillabs = sillabs
            # print(newsillabs[:-1])

            split_word = newsillabs[:-1].split('-')  # готовый список слогов

            shuf_w = split_word[:]
            random.shuffle(shuf_w)
            while shuf_w == split_word:  # мешаем слоги так, чтобы точно изменился порядок
                random.shuffle(shuf_w)

            shuf_w = '[' + ''.join(shuf_w) + ']'  # слово внутри задания
            key_w = '[' + stroka + ']'  # слово внутри ключей - тоже в скобочках, но в верном порядке

            shuf_w_token = fun.Token(shuf_w)
            key_w_token = fun.Token(key_w)

            return shuf_w_token, key_w_token
        else:
            return word, word


    def make_shuf_sents(old_words):
        shuf_words = [''] * len(old_words)
        key_words = shuf_words[:]

        for i, w in enumerate(old_words):
            shuf_words[i], key_words[i] = syllables(w, 2)

        return shuf_words, key_words  # списки токенов в предложении


    text = fun.reading("banya")
    sentences = fun.sts(text)
    tokens = fun.tkns(sentences)

    shuf_sents, key_sents = [], []
    for sentence in tokens:
        shuf_words, key_words = make_shuf_sents(sentence)
        shuf_sents.append(shuf_words)
        key_sents.append(key_words)
    #print(fun.join_toks(shuf_sents))
    #print(fun.join_toks(key_sents))

    # форматируем тексты задания и ключей
    task_text = task.format(fun.join_toks(shuf_sents))
    key_text = task.format(fun.join_toks(key_sents))

    if '[' not in task_text:
        task_text = task.format('К сожалению, в тексте нет ни одного подходящего слова. Попробуйте выбрать уровень выше или просто подобрать другой текст.')

    # записываем задание и ключи
    fun.writing(task_text, task_name)
    fun.writing_key(key_text, task_name)

    # выводим на сайт
    site_task_text = task_text.replace('\n', '<br>')
    print(site_task_text, "<br><br><br>")
    print("Ответы:<br>")
    site_key_text = key_text.replace('\n', '<br>')
    print(site_key_text)

    show_task_name = str(task_name) +'_show'
    fun.writing(site_task_text,show_task_name )
