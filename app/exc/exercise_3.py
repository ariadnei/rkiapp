def main():
    text = open('app/uploads/files/text.txt', encoding="utf-8").read()
    #print(text)

    import app.exc.functions as fun
    import pymorphy2, nltk
    morph = pymorphy2.MorphAnalyzer()

    text_z = 'Поставьте местоимение, прилагательное или числительное в скобках в нужную форму и заполните пропуски (1) - ({0}), как показано в примере (0). Обратите внимание, что ответом может являться форма, данная в скобках.'

    sentences = nltk.sent_tokenize(text) # делим текст на предложения
    # sentenses = ['sent.', '\n', 'sent!']

    tokens = fun.tkns(sentences) #делим предложения на токены
    # tokens = [['w', ',', ' '], [...]]
    #print(tokens)

    # Выбираем из текста все прилагательные и местоимения, рядом с которыми стоят существительные
    # tokens = [['w', ',', ' '], [...]]
    def adj_pron(tokens):
        prev_token = '' # предыдущий токен каждого слова
        word_sent = []
        for sentence in tokens:
            words = [] # все подходящие слова в предложени
            for token in sentence: # проверяем каждый токен в предложении
                if token.isalpha: # если токен -- слово и оно есть в списке 10 000 самых частотных
                    p_token = morph.parse(token)[0]
                    p_prev_token = morph.parse(prev_token)[0]
                    if p_token.tag.POS == 'ADJF' and p_prev_token.tag.POS == 'NOUN':
                        words.append(token)
                    if p_token.tag.POS == 'NOUN' and p_prev_token.tag.POS == 'ADJF':
                        words.append(prev_token)
                    if p_token.tag.POS == 'NPRO' and p_prev_token.tag.POS == 'NOUN':
                        words.append(token)
                    if p_token.tag.POS == 'NOUN' and p_prev_token.tag.POS == 'NPRO':
                        words.append(prev_token)
                    prev_token = token
            word_sent.append(words)
        return word_sent

    w_adj_pr = adj_pron(tokens)  # получаем список прилагательных и местоимений из предложений
    # w_adj_pr = [['w'], ['\nw1', 'w2'], [], [...]]
    #print(w_adj_pr)

    wlist = fun.rand_one(w_adj_pr) # выбираем по одному слову из предложения
    # wlist = ['w from s1], '', 'w from s2', '...']
    #print(wlist)

    # берём в пример первое непустое значение и удаляем его из списка ответов
    for w in wlist:
        if w.isalpha():
            example = w
            break # и выходим
    ans_list = wlist[1:] #список ответов

    res, k = fun.prop_norm(tokens, wlist, example) # добавили пропуски с леммами, подсчитали пропуски
    # res = [['\nw', '(1)______(лемма w)', ',', ' '], [' ', '\n'], [...]]
    # k = 7
    #print(res)

    sentences = fun.toks_sent(res) # склеили токены предложений в строки
    # res = [['\nw', '(1)______(лемма w)', ',', ' '], [' ', '\n'], [...]]
    # sentences = ['sent w ____ (1). ', '\n', 'sent! ___ (2)']


    task = fun.task(sentences, text_z, k) # склеили предложения в строку, добавили задание
    #task = '...'


    print(task, "<br><br><br>")
    f = open('app/uploads/to_download/task_3.txt', 'w')
    f.write(task)
    f.close()

    print("Ответы:<br>")

    f = open('app/uploads/to_download/answ_3.txt', 'w')
    for i in range(len(ans_list)):
        f.write(str(i+1)+")"+ ans_list[i] + '\n')
        print(str(i+1)+")", ans_list[i])
        print("<br>")
    f.close()
