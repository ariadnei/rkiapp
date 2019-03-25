'''
3. Собрать предложение из перемешанных слов.
'''

def main(level, coef):
    import app.site_ver.functions as fun
    import random

    task_name = 3
    task = 'Составьте предложение из слов, расположив их в правильном порядке. Обратите внимание, что вариантов может быть несколько!\n\n{}'

    text = fun.reading('text')
    #print(text)

    sents = fun.sts(text)
    #print(sents)

    tokens = fun.tkns(sents)
    #print(tokens)
    text_tokens = fun.text_tokens(tokens)
    #print(text_tokens)


    suit_sents = [] # список предложений, у которых коэффициент незнакмых значимых слов не меньше порога
    # TODO: для словоформ тоже нужно проверять, или не надо?
    for i, sent in enumerate(tokens):
        coef_sent = fun.coef_sent(sent, level, coef)
        #print(coef_sent)
        if coef_sent[0]:
            #print(fun.text_tokens(sent))
            suit_sents.append(i)
    #print(suit_sents)

    #TODO: продумать, как отбираем предложения и сколько
    if not suit_sents:  # все предложения слишком сложны
        print('К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте снизить коэффициент знакомых значимых слов, выбрать уровень выше или просто подобрать другой текст.')
        show_task_name = 'К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте снизить коэффициент знакомых значимых слов, выбрать уровень выше или просто подобрать другой текст.'

    else:
        to_shuf = random.choice(suit_sents)

        # получаем список лемм
        #TODO: сделать усложнённый вариант: без союзов и предлогов
        shuf_sent = [token.text.lower() for token in tokens[to_shuf] if not token.punct] # знаки препинания убираем
        #print(lem_sent)

        # перемешиваем леммы
        rand_words, _ = fun.shuffle(shuf_sent)
        #print(rand_words)

        task_text = ' '.join(rand_words)

        # в качестве ключа берём исходное предложение
        key = sents[to_shuf]

        # форматируем тексты задания и ключей
        task_text = task.format(task_text)
        key_text = task.format(key)

        # записываем задание и ключи
        fun.writing(task_text, task_name)
        fun.writing_key(key_text, task_name)

        # выводим на сайт
        site_task_text = task_text.replace('\n', '<br>')
        print(site_task_text, "<br><br><br>")
        print("Ответы:<br>")
        site_key_text = key
        print(site_key_text)

    show_task_name = str(task_name) +'_show'
    fun.writing(site_task_text,show_task_name )
