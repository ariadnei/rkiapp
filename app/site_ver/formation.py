# должна быть предустановлена библиотечка xlrd
import pandas as pd
from collections import defaultdict

slovar = pd.read_excel('app/site_ver/data/Список.xlsx')
#print(slovar)

slovar = slovar.fillna('') # заменяем пустые на ''
#print(slovar)

vocab = {} # все дериваты с начальными словами
# TODO: запилить класс?
deriv = defaultdict(list) # {'слово': [дериваты]}
pref = defaultdict(list) # {'слово': [приставки дериватов]} '', если у деривата нет приставки
stem = defaultdict(list)
suf = defaultdict(list)
end = defaultdict(list)
stress = defaultdict(list)

for i in range(len(slovar)):
    word = slovar['слово'][i]
    #print(word)
    der = slovar['дериват'][i] # дериват слова
    if word != der: # если в списках дериватов не попалось само слово (а то заменять бестолку)
        deriv[word].append(der)
        vocab[der] = word
        pref[word].append(slovar['приставка'][i])
        stem[word].append(slovar['основа'][i])
        suf[word].append(slovar['суффикс'][i])
        end[word].append(slovar['окончание'][i])
        stress[word].append(slovar['ударение'][i])

#print(deriv)
#print(stem)
#print(stress)
#print(vocab)
