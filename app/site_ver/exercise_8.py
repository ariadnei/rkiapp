'''
8. Проставить ударение
'''

def main(level):
    import app.site_ver.functions as fun
    import app.site_ver.formation as form

    task_name = 8
    task = 'Поставьте ударение в выделеных словах (1) - ({}).\n\n{}'

    text = fun.reading('text')
    #print(text)

    sents = fun.sts(text)
    #print(sents)

    tokens = fun.tkns(sents)
    #print(tokens)
    text_tokens = fun.text_tokens(tokens)
    #print(text_tokens)


    new_tokens = [] # пойдёт в задание
    key_tokens = [] # пойдёт в ключи
    k = 0  # счётчик номеров
    for sent in tokens:
        new_sent = []
        for token in sent:
            #print(token.text, token.lem)
            if fun.check_min(token.lem, level) and token.lem in form.vocab:
                #print(True) #TODO: всё, кроме пара, в B1 добавлено искусственно для игрушечного теста -- удалить!
                k += 1
                new_token = fun.Token('({})_{}_'.format(k, token.text)) # делаем новым токеном то же слово с подчёркиванием
                #print(new_token.text)

                # key_token -- подчёркнут ударный гласный

                main_w = form.vocab[token.lem] # начало словообразовательной цепочки
                deriv_n = form.deriv[main_w].index(token.lem) # номер токена в словарных списках
                #print(deriv_n)
                stress = form.stress[main_w][deriv_n]
                #print(stress)
                counter = 0  # счётчик гласных в слове
                i = -1  # позиция ударного гласного
                while i < len(token.text) - 1 and counter < stress:  # пока проверили не все буквы и не дошли до нужного гласного
                    i += 1
                    #print(i, word[i], counter)
                    if token.text[i] in fun.vowels:
                        counter += 1
                #print(stress, i)
                key_token = '({}) {}_{}_{}'.format(k, ''.join(token.text[:i]), ''.join(token.text[i]), ''.join(token.text[i + 1:]))

                new_sent.append(new_token)
                key_tokens.append(key_token)
            else:
                new_sent.append(token)
        new_tokens.append(new_sent)
    #print(fun.text_tokens(new_tokens))
    #print(key_tokens)

    if k == 0: # если не пометили ли слова
        print('К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте выбрать уровень выше или просто подобрать другой текст.')
        site_task_text = 'К сожалению, в тексте нет ни одного предложения, подходящего для создания упражнения. Попробуйте выбрать уровень выше или просто подобрать другой текст.'

    else:
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
