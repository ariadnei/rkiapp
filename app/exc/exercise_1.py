def main():

    from django.http import HttpResponse
    text = open('app/uploads/files/text.txt', encoding="utf-8").read()

    import app.exc.functions as fun
    import pymorphy2
    import nltk
    morph = pymorphy2.MorphAnalyzer()

    text_z = 'Определите род слов и впишите ответы в пропуски (1) - ({0}), как показано в примере (0).'

    sentences = nltk.sent_tokenize(text)

    #print(sentences)

    tokens = fun.tkns(sentences) #делим предложения на токены
    # tokens = [['w', ',', ' '], [...]]
    #print(tokens)


    # определяем все слова, имеющие род. Если в предложении таких нет -- пустой список
    # tokens = [['w', ',', ' '], [...]]
    def rod(tokens):
        word_sent = [] # список предложений со словами, для которых можно определить род

        for sentence in tokens:
            words = [] # все слова в предложении, для которых определяется род
            for token in sentence:
               if token.isalpha : #  and fun.check(token)  если токен -- слово, и оно есть в списке 10 000 наиболее частотных
                   p = morph.parse(token)[0]
                   #print(p.tag)
                   # работаем с:
                   # -- существительными с выраженным родом,
                   # -- полными и краткими (НЕ среднего рода, чтобы не было совпадений с наречиями) прилагательными единственного числа,
                   # -- полными и краткими причастиями единственного числа,
                   # -- глаголами единственного числа, 3 лица, прошедшего времени
                   # ПРИШЛОСЬ ПРОПИСАТЬ ОТСУТСТВИЕ МЕСТОИМЕНИЙ, Т.К. ИНАЧЕ НИКАК НЕ УДАЁТСЯ ИСКЛЮЧИТЬ "я" (возможно, другие местоимения тоже)
                   if ((p.tag.POS == 'NOUN' and 'GNdr' not in p.tag)or (p.tag.POS == 'ADJF' and p.tag.number == 'sing') or (p.tag.POS == 'ADJS' and p.tag.number == 'sing' and p.tag.gender != 'neut') or (p.tag.POS == 'PRTF' and p.tag.number == 'sing') or (p.tag.POS == 'PRTS' and p.tag.number == 'sing') or (p.tag.POS == 'NPRO' and p.tag.number == 'sing') or (p.tag.POS == 'VERB' and p.tag.number == 'sing' and p.tag.tense == 'past' and p.tag.person == '3per')) and p.tag.POS != 'NPRO' :
                      #print(token)
                      words.append(token)
            word_sent.append(words)
        return word_sent

    w_rod = rod(tokens) # получаем списки слов с родом из предложений
    # w_rod = [['w', 'w'], [], [...]]
    #print(w_rod)


    wlist = fun.rand_one(w_rod) # выбираем по одному подходящему слову из предложения
    # wlist = ['w from s1], '', 'w from s2', '...']
    #print(wlist)


    # заменяем обозначения родов pymorphy на привычные
    glist = [] # список родов слов
    for w in wlist:
        if w.isalpha:
            p = morph.parse(w)[0]
            if p.tag.gender == 'femn':
                g = 'ж. р.'
            elif p.tag.gender == 'masc':
                g = 'м. р.'
            elif p.tag.gender == 'neut':
                g = 'ср. р.'
            elif 'Ms-f' in p.tag: # если слово общего рода
                g = 'общ.р.'
            else:
                g = None
            glist.append(g)

    # берём в пример первое непустое значение glist и удаляем его из списка ответов
    for w in glist:
        if w!=None:
            example = w
            break # и выходим

    res, k = fun.prop(tokens, wlist, example) # добавили пропуски, подсчитали их число
    # res = [['\nw', 'w ______ (1)', ',', ' '], [' ', '\n'], [...]]
    # k = 7

    sentences = fun.toks_sent(res) # склеили токены предложений в строки
    # res = [['\nw', 'w ______ (1)', ',', ' '], [' ', '\n'], [...]]
    # sentences = ['sent w ____ (1). ', '\n', 'sent! ___ (2)']
    #print(sentences)
    task = fun.task(sentences, text_z, k) # склеили предложения в строку, добавили задание
    #task = '...'

    print(task, "<br><br><br>")

    f = open('app/uploads/to_download/task_1.txt', 'w')
    f.write(task)
    f.close()

    print("Ответы:")

    f = open('app/uploads/to_download/answ_1.txt', 'w')
    for i in range(1, len(wlist)):
        if wlist[i] != '':
            f.write(str(i)+")"+ wlist[i]+"-" + glist[i] + '\n')
            print(str(i)+")", wlist[i],"-", glist[i])
    f.close()

    return HttpResponse('<h2>Упражнение номер 1</h2>')
