def main():
    text = open('app/uploads/files/text.txt', encoding="utf-8").read()

    import pymorphy2, nltk
    import app.exc.functions as fun
    import random
    morph = pymorphy2.MorphAnalyzer()

    text_z = 'Поставьте глаголы в скобках в нужную форму и заполните пропуски (1) - ({0}), как показано в примере (0). Обратите внимание, что ответом может являться форма, данная в скобках.'


    sentences = nltk.sent_tokenize(text)
    tokens = fun.tkns(sentences)
    #print(tokens)


    # выбираем из каждого предложения все глаголы
    def list_verbs(tokens):
        list_of_verbs = []  # список списков глаголов в каждом предложении
        for sentence in tokens: # для каждого предложения
            #print(sentence)
            verbs_in_sent = [] # список глаголов в предложении
            for word in sentence: # проверяем каждое слово в предложении
            #print(verb)
                p = morph.parse(word)[0]
                pos = p.tag
                #print(p.tag.POS)
                if p.tag.POS == 'VERB': # если слово -- глагол и есть в списке 10 000 наиболее частотных
                    verbs_in_sent.append(word)
            list_of_verbs.append(verbs_in_sent)
        return list_of_verbs

    list_of_verbs = list_verbs(tokens) # получаем списки глаголов из предложений
    # print(list_of_verbs)
    # list_of_verbs = [['w1 from sent 1', 'w2 from sent2'], [], [w1 from sent3], ...]
    vlist = fun.rand_one(list_of_verbs) # выбираем по одному глаголу из предложения
    # print(vlist)
    # vlist = ['verb from sent1, '', 'verb from sent2']

    # берём в пример первое непустое значение и удаляем его из списка ответов
    for w in vlist:
        #print(w)
        if w.isalpha():
            example = w
            break # и выходим
    ans_list = vlist[1:]

    res, k = fun.prop_norm(tokens, vlist, example) # добавляем пропуски с лемами в скобках, считаем количество пропусков
    #print(res)
    # res = [['\nw', '(1)______(лемма w)', ',', ' '], [' ', '\n'], [...]]
    # k = 7

    sentences = fun.toks_sent(res) # склеили токены предложений в строки
    # res = [['\nw', '(1)______(лемма w)', ',', ' '], [' ', '\n'], [...]]
    # sentences = ['sent w ____ (1). ', '\n', 'sent! ___ (2)']

    task = fun.task(sentences, text_z, k) # склеиваем предложения в строку, добавляем задание
    # task = '...'


    print(task, "<br><br><br>")

    f = open('app/uploads/to_download/task.txt', 'w')
    f.write(task)
    f.close()

    print("Ответы:<br>")

    f = open('app/uploads/to_download/answ.txt', 'w')
    for i in range(len(ans_list)):
        f.write(str(i+1)+")"+ ans_list[i] + '\n')
        print(str(i+1)+")", ans_list[i])
        print("<br>")
    f.close()
