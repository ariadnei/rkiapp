import nltk
#nltk.download('punkt')
import spacy
import random
from os import makedirs

# знаки препинания, перед которыми не нужен пробел
punct_next = ['.', '!', '?', ',', '"', '»', ';', ':', ')', ']', '}', '...', '!..', '?..', '&', '@', "'"]
# знаки препинания, после которых не нужен пробел
punct_prev = ['"', '«', '(', '[', '{', '&', '@', "'"]

vowels = ['а', 'е', 'и', 'о', 'у', 'я', 'э', 'ы', 'ё', 'ю']

levels = ['A1', 'A2', 'B1', 'B2'] #TODO: пополнить

model_path = "C:\\Users\\asus\\Documents\\SpaCy\\buriy\\ru2"
ru_spacy = spacy.load(model_path) # загрузим языковую модель

# Формируем множества минимумов
# mins = {'A1': {'w1', 'w2', ...}, 'A2': {...}}
mins = {}
for level in levels:
    min = open("data\\{}.txt".format(level), encoding='utf-8').read().lower().split('\n') # получаем список слов
    mins[level] = set(min)
#print(mins)


# Проверяем, есть ли слово в минимуме уровня
def check_min(w, level):
    if w.lower() in mins.get(level):
        return True
    else:
        return False

# читает из файла, убирает двойные пробелы и ручные переносы, последний \n на пустую строчку
def reading(file):
    f = open('app/uploads/files/{}.txt'.format(file), 'r', encoding='utf-8')
    text = f.read()
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.replace('-\n', '')
    if text[-1] == '\n': # убираем последний \n на пустую строчку
        text = text[:-1]
    f.close()
    return text


# сплитим предложения, сохраняя \n для абзацев как отдельные предложения
def sts(text): #TODO: предусмотреть некоррекнотсти текста
    # не делит предложения, если после знака препинания нет пробела
    # не считает многоточие концом предложения
    text = text.replace('\n', ' %^&. ') # для сохранения \n #TODO: добавить точку, чтобы \n всегда уходил в отдельное предложение
    sentences = []
    for sent in nltk.sent_tokenize(text):
        #print(sent)
        if sent != '%^&.' and '%^&.' in sent: # если знак-заместитель остался в нормальном предложении
            sentences.append(sent[:-5]) # добавляем их отдельно
            sentences.append('%^&.')
        else:
            sentences.append(sent)

    return sentences


def parse_tag(tag): # получаем все грамемы слова в виде словаря
    #print(tag)
    gram = {}
    analysis = tag.split('__')[-1] # убираем приставку с pos-тегом
    gramems = analysis.split('|')
    #print(gramems)
    if gramems[0] != '' and gramems[0] != '_': # токен разбирается
        for gramem in gramems:
            property, feature = gramem.split('=')
            gram[property] = feature
        #print(gram)
    return gram

class Token():
    def __init__(self, w):
        if isinstance(w, spacy.tokens.token.Token): # если получили токен spacy
            self.text = w.text  # сам токен
            self.lem = w.lemma_  # лемма
            self.pos = w.pos_  # часть речи
            self.gram = parse_tag(w.tag_) # грам разбор в виде словаря
            self.syntax = w.dep_  # синтакс. роль
            self.digit = w.is_digit  # число ли
            self.alpha = w.is_alpha  # буквы ли
            self.stop_word = w.is_stop # стоп-слово ли
            self.title = w.is_title # начинается с заглавной
            self.punct = w.is_punct # знак препинания
            self.original = w
        else:
            self.text = w # задаём саму строку текстом токена

        self.num = None # номер в предложении


def tkns(sents):
    tokens = []
    for sent in sents:
        sent = sent.replace('%^&.', '\n') # восстанавливаем \n
        parsed = ru_spacy(sent)  # сохраняет пунктуацию, \n, слова через апостроф считает одним
        # не сохраняет пробелы, не делит токены, если между ними знак препинания без пробела
        toks = []
        for i, w in enumerate(parsed): # состаляем список объектов Tokens
            token = Token(w)
            #print(token.text)
            #print(token.gram)
            token.num = i # добавляем токену в атрибуты его номер в предложении
            toks.append(token)
        tokens.append(toks)

    return tokens

def text_tokens(tokens): # печатает список списков объектов Tokens текcтом
    #print(tokens[0])
    #print(type(tokens[0]))
    if isinstance(tokens[0], list): # если внутри вложенный список
        text_tokens = [] # собираем список списков
        for toks in tokens:
            sent = []
            for tok in toks:
                if isinstance(tok, Token):
                    sent.append(tok.text)
                else:
                    sent.append(tok)
            text_tokens.append(sent)
    else:
        text_tokens = [] # собираем простой список
        for tok in tokens:
            if isinstance(tok, Token):
                text_tokens.append(tok.text)
            else:
                text_tokens.append(tok)
    return text_tokens


# считает отношение слов из минимума ко всем значимым словам в предложении
# ПРОВЕРЯТЬ IF С ИНДЕКСАЦИЕЙ, fun.coef_sent(sent, 'B2')[0] -- иначе всегда True, т.к. возвращает кортеж
def coef_sent(sentence, level, threshold = 0.8):
    meaningful = [token for token in sentence if token.alpha and not token.stop_word and token.text != '\n']
    if meaningful: # если набрались знаменательные слова
        known = [token for token in meaningful if check_min(token.lem, level)]
        #print(text_tokens(meaningful)) # значимые слова
        #print(text_tokens(known)) # слова из минимума
        coef = len(known) / len(meaningful)
        if coef >= threshold:
            return True, coef
        else:
            return False, coef
    else:
        coef = 0
        return False, coef


# рандомно берёт по одному подходящему слову из списка для предложения, если таких нет -- пустая строка
# w_in_sent = [['w', 'w'], [], [...]]
# w_list = ['w from s1], '', 'w from s3', '...']
def rand_one(w_in_sent):
    w_list = [] # список по одному слову из предложения
    for sent in w_in_sent:
        try: # выбираем слово для предложения
            word = random.choice(sent) # TODO: нужна ли проверка на уникальность вообще?
            while word in w_list: # если такое слово уже брали:
                sent.remove(word) # удаляем из списка возможных
                word = random.choice(sent)
            w_list.append(word)
        except IndexError: # если для этого предложения нет слова
            w_list.append('')
    return w_list


# возвращает перемешанные элементы и правильную расстановку этих элементов
def shuffle(elements):
    rand_elements = random.sample(elements, len(elements))
    while rand_elements == elements:  # защита от случайного повторения исходного порядка
        rand_elements = random.sample(elements, len(elements))
    # возвращаем заодно правильный порядок
    right_elements = []
    for i, element in enumerate(elements):
        num = rand_elements.index(element)
        right_elements.append(num + 1)
    return rand_elements, right_elements


# склеивает предложение как список токенов в предложение как строку
# получает список списков
# склеивает предложение как список токенов в предложение как строку
# получает список списков
def join_toks(tokens):
    sentences = []
    for toks in tokens:
        sent = ""
        for e in toks:
            if not 'а' <= e.text[0].lower() <= 'я':
                if e.text[0] in punct_next:
                    sent = sent.strip() + e.text + " "
                elif e.text[-1] in punct_prev:
                    sent += e.text
                else:
                    sent += e.text + " "
            else:
                sent += e.text + " "
        if sent[-1] == ' ': # strip режет \n тоже
            sent = sent[:-1]
        sentences.append(sent)
    return sentences

'''
def join_toks(tokens):
    sentences = []
    for toks in tokens:
        sent = toks[0].text # сразу добавляем первый токен
        #print(sent)
        for i, tok in enumerate(toks[1:]): # для каждого токена в предложении, не считая первого
            #print(tok.text)
            """
            i-1      i
            prev    next
             -       -      ' 'tok
             -       +      tok
             +       -      tok
             +       +      tok
            """
            if (toks[i-1].text not in punct_prev) and (toks[i].text not in punct_next): # если после предыдущего токен можно пробел и перед следующим можно
                #print('Можно пробел')
                sent += ' ' # добавляем пробел
            sent += tok.text # добавляем текст токена
            #print(sent)
        sentences.append(sent)
    return sentences
'''

# создаёт строку с пронумерованным списком ответов
def list_key(key):
    keys = ''
    for i, k in enumerate(key):
        keys += '{}) {}\n'.format(i + 1, k)
    keys = keys[:-1]
    return keys


# записывает в файл task_name упражнение
def writing(task, task_name):
    f = open('app/uploads/to_download/{}.txt'.format(task_name), 'w', encoding='utf-8')
    f.write(task)
    f.close()

# записывает в файл task_name_key ключи
def writing_key(key, task_name):
    f = open('app/uploads/to_download/{}.txt'.format(task_name), 'w', encoding='utf-8')
    f.write(key)
    f.close()