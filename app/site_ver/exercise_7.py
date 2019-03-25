'''
7. Образовать слова от слов в скобках и ставить в пропуски
'''

def main(level):
    import app.site_ver.functions as fun
    import app.site_ver.formation as form

    task_name = 7
    task = 'Вставьте в пропуски (1) - ({}) слова, образованные от слов в скобках. Поставьте эти слова в правильную форму.\n\n{}'
    #TODO: добавить заполненный пример

    text = fun.reading('text')
    #print(text)

    sents = fun.sts(text)
    #print(sents)

    tokens = fun.tkns(sents)
    #print(tokens)
    text_tokens = fun.text_tokens(tokens)
    #print(text_tokens)


    w_in_sent = [] # список всех подходящих слов в предложениях
    for sent in tokens:
        w_for_sent = [] # список подходящих в предложении; пустой, если ничего
        for token in sent:
            if fun.check_min(token.lem, level) and token.lem in form.vocab:
                w_for_sent.append(token) # добавляем срзу весь токен
        w_in_sent.append(w_for_sent)

    #print(w_in_sent)

    w_list = fun.rand_one(w_in_sent)
    #print(w_list)

    suit_n = '' # проверяем, есть ли хоть одно реальное слово в w_list, или все ''
    for e in w_list:
        suit_n += str(e)

    if not suit_n: # ни в одном предложении ни нашлось ни одного подходящего слова
        print('К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте выбрать уровень выше или просто подобрать другой текст.')
        site_task_text = 'К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте выбрать уровень выше или просто подобрать другой текст.'

    else:
        new_tokens = [] # пойдёт в задание
        key_tokens = [] # пойдёт в ключи
        k = 0  # счётчик номеров
        for i, sent in enumerate(tokens): # заменяем на пропуски
            if w_list[i]: # есть токен на замену
                k += 1
                root_word = form.vocab[w_list[i].lem]
                #print(w_list[i].text, root_word)
                new_token = fun.Token('({})______({})'.format(k, root_word))  # делаем новым токеном то же слово с подчёркиванием
                #print(new_token.text)
                new_sent = sent[:w_list[i].num] + [new_token] + sent[w_list[i].num+1:]
                new_tokens.append(new_sent)

                key_token = '({}) {}'.format(k, w_list[i].text)
                key_tokens.append(key_token)
            else:
                new_tokens.append(sent)

        #print(fun.text_tokens(new_tokens))
        #print()
        #print(key_tokens)


        task_text = fun.join_toks(new_tokens)
        #print(task_sents)

        #task_text = ' '.join(task_sents)
        #print(task_text)

        key_text = '\n'.join(key_tokens)
        #print(key_text)

        # форматируем тексты задания и ключей
        task_text = task.format(k, task_text)
        key_text = task.format(k, key_text)

        # записываем задание и ключи
        fun.writing(task_text, task_name)
        fun.writing_key(key_text, task_name)

        # выводим на сайт
        site_task_text = task_text.replace('\n', '<br>')
        print(site_task_text, "<br><br><br>")
        print("Ответы:<br>")
        site_key_text = '<br>'.join(key_tokens)
        print(site_key_text)

    show_task_name = str(task_name) +'_show'
    fun.writing(site_task_text,show_task_name )
