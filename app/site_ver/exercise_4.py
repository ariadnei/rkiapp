'''
4. Составить предложения из лемм. Для усложнения: из задания убраны все предлоги, надо вставить самим.
'''

def main(level, coef):
    import app.site_ver.functions as fun
    import random

    task_name = 4
    task = 'Составьте предложение из слов, поставив их в нужную форму. Обратите внимание, что вариантов может быть несколько!\n\n{}'

    text = fun.reading('text')
    #print(text)

    sents = fun.sts(text)
    #print(sents)

    tokens = fun.tkns(sents)
    #print(tokens)
    text_tokens = fun.text_tokens(tokens)
    #print(text_tokens)


    suit_sents = [] # список предложений, у которых коэффициент незнакмых значимых слов не меньше порога
    for i, sent in enumerate(tokens):
        coef_sent = fun.coef_sent(sent, level, coef)
        #print(coef_sent)
        if coef_sent[0]:
            #print(fun.text_tokens(sent))
            suit_sents.append(i)
    #print(suit_sents)

    #TODO: продумать, как отбираем предложения и сколько
    if not suit_sents:
        print('К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте снизить коэффициент знакомых значимых слов, выбрать уровень выше или просто подобрать другой текст.')
        show_task_name = 'К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте снизить коэффициент знакомых значимых слов, выбрать уровень выше или просто подобрать другой текст.'

    else:
        to_lem = random.choice(suit_sents)

        # получаем список лемм
        #TODO: сделать усложнённый вариант: без союзов и предлогов
        lem_sent = [token.lem for token in tokens[to_lem] if not token.punct] # знаки препинания убираем
        #print(lem_sent)

        # перемешиваем леммы
        rand_lems, _ = fun.shuffle(lem_sent)
        #print(rand_lems)

        task_text = ' '.join(rand_lems)

        # в качестве ключа берём исхожное предложение
        key = sents[to_lem]

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
