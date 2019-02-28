import random
import nltk
import pymorphy2
morph = pymorphy2.MorphAnalyzer()

# знаки препинания, перед которыми не нужен пробел
punct_next = ['.', '!', '?', ',', '"', '»', ';', ':', ')', ']', '}', '...', '!..', '?..', '&', '@']

# знаки препинания, после которых не нужен пробел
punct_prev = ['"', '«', '(', '[', '{', '&', '@']

# Формируем множество 20 000 самых частотных слов
# freq_w = ('w1', 'w2', ...)
file = open("app/exc/20000words.txt", "r")
text = file.read().split('\n') # получаем список слов
file.close()
freq_w = set(text)
#print(freq_w)

# Проверяем, есть ли слово во множестве самых частотных
def check(w, check_list = freq_w):
    if str(w).lower() in check_list:
        return True
    else:
        return False

#  читает из файла, убирает двойные пробелы и ручные переносы
# file= 'name.txt'
# text = '...'
def reading(file):
    f = open(file, 'r', encoding='utf-8')
    text = f.read()
    while '  ' in text:
        text = text.replace('  ', ' ')
        text = text.replace('-\n', '')
    f.close()
    return text

'''
# делит текст на предложения
# text = '...'
# sentenses = ['sent. \n', ' \n', 'sent! ']
def sts(text):
    n = 0
    fsentences = []
    for i in range(len(text)):
        if (text[i-2] == '!') or (text[i-2] == '?') or (text[i-2] == '.') or (text[i-2] == '\n'):
            if (text[i-1] == ' ') and ((text[i].isupper() == True) or (text[i] == '"')):
                fsentences.append(text[n:i-1])
                n = i
            if (text[i-1].isupper() == True) or (text[i] == '"'):
                fsentences.append(text[n:i-1])
                n = i-1
    for i in range(len(text)):
        b = text[-2-i:]
        if (b[1].isupper() == True) and ((b[0] == ' ') or (b[0] == '\n') or (b[0] == '"')):
            fsentences.append(text[-2-i:])
            break
    sentences = []
    for s in range(len(fsentences)):
        if len(fsentences[s])>0:
            if ('\n' in fsentences[s]) and (len(fsentences[s])>1):
                sentences.append(fsentences[s][:-1])
                sentences.append('\n')
            else:
                sentences.append(fsentences[s])
    return sentences
'''

# делит текст на предложения
# удаляет пробелы после точки и \n
# text = '...'
# sentenses = ['sent.', 'sent!']
def stsk(text):
    text2 = ''
    n = 0
    for i in range(len(text)):
        if text[i] == '\n':
            text2 = text2+text[n:i]+' %^&.'+' '
            n = i+1
    sentences = nltk.sent_tokenize(text2)
    return sentences


# делит предложения на токены
# sentenses = ['sent. \n', ' \n', 'sent! ']
# tokens = [['\nw', ',', ' '], [' ', '\n'], [...]]
def tkns(sentences):
    n = 0
    j = 0
    tokens = []
    for s in sentences:
        n=0
        tokens.append([])
        for i in range(len(s)):
            if (s[i] == ' '):
                tokens[j].append(s[n:i])
                n = i+1
            if (s[i]==',') or (s[i]==':') or (s[i]==';') or (s[i]=='/t') or (s[i]=='.') or (s[i]=='!') or (s[i]=='?'):
                '''if (s[i-1]=='.'):
                    print('n', n, s[n])
                    print('i', i, s[i])
                    print ('s-1', s[i-1])
                    print ('s', s[i])
                    tokens[j].append(s[i-1])
                    tokens[j].append(s[i])
                    n = i
                else:
                    tokens[j].append(s[n:i])
                    tokens[j].append(s[i])
                    n = i+1'''
                if (s[i]=='.') or (s[i]=='!') or (s[i]=='?'):
                    tokens[j].append(s[n:i])
                    tokens[j].append(s[i])
                    if i+1 == len(s):
                        j+=1
                    n = i+1
                else:
                    tokens[j].append(s[n:i])
                    tokens[j].append(s[i])
                    n = i+1
            if (s[i]=='"') or (s[i]=='(') or (s[i]==')'):
                tokens[j].append(s[n:i])
                tokens[j].append(s[i])
                n = i+1
            if (s == '\n'):
                tokens[j].append(s)
                j+=1
    for t in tokens:
        if len(t) == 0:
            tokens.remove(t)
        for h in t:
            if (h == '') or (h == ' '):
                t.remove(h)
    return tokens

# делит предложение на токены
# убирает \n и пробелы после точек
# sentenses = ['sent. ', '\nsent! ']
# tokens = [['w', '!'], [...]]
def tknsk(sentenses):
    tokens = []
    for sent in sentenses:
        tks = nltk.word_tokenize(sent)
        tokens.append(tks)
    return tokens


# рандомно берёт по ОДНОМУ подходящему слову из предложения, если в предложении подходщих слов нет -- пустая строка
# w_in_sent = [['w', 'w'], [], [...]]
# wlist = ['w from s1], '', 'w from s3', '...']
def rand_one(w_in_sent):
    #print(w_in_sent)
    wlist = []
    check_povtor = set() # множество уже использованных словоформ
    for s in w_in_sent: # для каждого предложения
        #print('s = ',s)
        #print('l = ', len(s))
        if len(s)>=2:
            choice_from = s # из этого списка можно выбирать слова
            #print(choice_from)
            #print(s)
            k = len(wlist) # текущая длина wlist, т.е количество слов, которые мы уже отобрали
            #print(k)
            while len(wlist) == k: # до тех пор, пока мы не положили новое слово в wlist
                if len(choice_from)>0: #и пока остались слова, из которых можно выбирать
                    w = random.choice(choice_from) # выбираем новое рандомное слово из подходящих
                    #print(w)
                    choice_from.remove(w) # удаляем слово из списка
                    #print(choice_from)
                    if w not in check_povtor:
                        wlist.append(w)
                        #print(wlist)
                        check_povtor.add(w)
                        #print(check_povtor)
                else:
                    wlist.append('')
        elif len(s) == 1: # если в предложении только одно подходящее слово, то мы просто добавляем его в список
            if s[0] not in check_povtor:
                wlist.append(str(s[0])) # добавляем это слово
                check_povtor.add(s[0])
            else:
                wlist.append('')
        else: # если в предложении вообще нет подходящих слов, т.е. s = []
            wlist.append('')

    return wlist


# вставляет рядом со словом пропуск, подсчитывает число пропусков
# tokens = [['\nw', ',', ' '], [' ', '\n'], [...]]
# wlist = ['w from s1', '', 'w from s3', '...']
# tokens = [['\nw', ' ____(1)', ',', ' '], [' ', '\n'], [...]]
def prop(tokens, wlist, example):
    k = 0 # счётчик пропусков
    prop = ' ____________({0})' #  ______(1)
    for i in range(len(tokens)):
        if wlist[i] == '': #если в предложении нет подходящих слов
            pass
        else:
            sentence = tokens[i] # находим соответствующий список токенов
            #print(i, sentence)
            p = sentence.index(wlist[i]) # находим индекс нужного слова
            #print(wlist[i])
            sentence.insert(p+1, prop.format(k)) # вставляем после него пропуск
            #print(sentence)
            if k == 0:
                sentence[p+1] = ' ____' + example + '____(0)'
            tokens[i] = sentence # вставляем изменённое предложение
            #print(tokens[i])
            #print()
            k = k+1 # увеличиваем счётчик пропусков
    return tokens, k

# вставляет вместо слова пропуск и лемму изначального слова, подсчитывает число пропусков
# tokens = [['\nw', 'w' ',', ' '], [' ', '\n'], [...]]
# wlist = ['w from s1], '', 'w from s2', '...']
# tokens = [['\nw', '(1)______(лемма w)', ',', ' '], [' ', '\n'], [...]]
def prop_norm(tokens, wlist, example):
    k = 0 # счётчик пропусков
    prop = ' ({0})____________ ({1})' # (1)________ (лемма)
    for i in range(len(tokens)):
        if wlist[i] == '': # если в предложении нет подходящего слова
            pass
        else:
            word = morph.parse(wlist[i])[0]
            lem = word.normalized[0] #находим лемму первого разбора
            sentence = tokens[i] # находим соответствующий список токенов
            #print(sentence)
            p = sentence.index(wlist[i]) # находим индекс нужного слова
            #print(i)
            sentence[p] = prop.format(k, lem) # вставляем вместо него пропуск с леммой
            #print(sentence)
            if k == 0:
                sentence[p] = ' (0)____'+example+'____('+lem+')'
            tokens[i] = sentence # вставляем изменённое предложение
            #print(tokens[i])
            k = k + 1
    return tokens, k


# склеивает предложение как список токенов в предложеие как строку
# tokens = [['\nw', 'w ______ (1)', ',', ' '], [' ', '\n'], [...]]
# sentences = ['sent w ____ (1). ', '\n', 'sent! ___ (2)']
def toks_sent(tokens):
    sentences = [] # список предложений
    for sent in tokens: # для каждого предложения
        ansent = sent
        if sent[-2] == '%^&':
            if len(sent)==2:
                ansent = '\n'
            '''#sentence = sent[:-2]+'\n'
            else:
                sent.remove(sent[-1])
                sent.remove(sent[-1])
                ansent = sent
                ansent.append('\n')'''

        sentence = ansent[0] # текущее предложение -- первый токен
        #if sent == ['%^&', '.']:
            #sentence = '\n'
        for tok in range(1, len(ansent)-1): # для каждого токена в предложении, не считая первого и последнего
            #print(sentence)
            #print(sent[tok])
            #print(sent[tok].isalpha())
            #print()
            if ansent[tok-1] not in punct_prev and ansent[tok] not in punct_next: # если предыдущий токен -- не скобки/кавычки и т.д., а текущий -- не знак препинания
                sentence = sentence + ' ' # добавляем после первого токена пробел
            sentence = sentence + ansent[tok] # добавляем текущий токен к имеющейся строке
            #print(sentence)
            #print()
        sentence = sentence + ansent[-1]
        if sentence == '\n\n':
            sentence = '\n'
        if '%^&' in sentence:
            sentence = sentence[:-4]+'\n'
        sentences.append(sentence) # добавляем очередное предложение в список
        #print(sentences)
    return sentences


# склеивает предложения в строку, добавляет форматированный текст задания
# sentences = ['sent w ____ (1). ', '\n', 'sent! ___ (2)']
# text_z = 'Заполите пропуски (1) - (7).'
# text = '...'
def task(sentences, text_z, k=None): # если в задании нет пропусков, то k не требуется
    if k != None: # если необходимо подставить число пропусков
        text_z = text_z.format(k-1) # помним, что заполняем с 1, а не с 0
    #print(text_z)
    text = ''
    for i in sentences:
        text = text + ' ' + str(i)
    text = text[1:]
    text = text_z + '\n\n' + text #добавляем текст задания
    # убираем возможные двойные прбелы
    while text != text.replace('  ', ' '):
         text = text.replace('  ', ' ')
    text = text.replace('\n ', '\n')
    return text


# записывает в файл task_name текст упражнеия
# task = '...'
# key_name = 'name.txt')
def writing(task, task_name):
    f = open(task_name, 'w', encoding='utf-8')
    f.write(task)
    f.close()

# записывает в файл key_name ответы вида 1) изначальное слово\n 2) изначальное слово
# ans_list = ['answer from s1], '', 'answer from s2', '...']
# key_name = 'name_keys.txt')
def keys(ans_list, key_name):
    ans_list = list(filter(None, ans_list)) # отметаем все пустые строки
    key_list = []
    for num, ans in enumerate(ans_list, 1):
            key_list.append('{0}) {1}\n'.format(num, ans))
    with open(key_name, "w", encoding='utf-8') as f:
        for word in key_list:
            f.write(word.lower())
    f.close()

# записывает в файл key_name текст ключей
# key_text = '...'
# key_name = 'name.txt')
def keys_text(key_text, key_name):
    f = open(key_name, 'w', encoding='utf-8')
    f.write(key_text)
    f.close()
