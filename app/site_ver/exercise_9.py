def main(rang, count):
    import app.site_ver.functions as fun
    from random import randint
    import re

    task_name = 9
    task = 'Напишите словами следующее число:\n\n{}'

    def divide_on_three(number):
        number = str(number)[::-1]
        lst = [number[i: i + 3][::-1] for i in range(0, len(number), 3)]
        #lst = lst[::-1]
        return [int(e) for e in lst]

    def convert_to_words(num):
        result = []
        if num in dct:
            result.append(dct[num][0])
        else:
            result.append(dct[100 * (num // 100)][0])
            if num % 100 in dct:
                result.append(dct[num % 100][0])
            else:
                result.append(dct[10 * ((num % 100) // 10)][0])
                result.append(dct[((num % 100) % 10)][0])
        return (result, num)

    def add_inflections(num, rank, lst):
        if rank == 2:
            if (num % 100) % 10  == 1 and num % 100 != 11:
                lst[len(lst) - 1] = dct[(num % 100) % 10][1]
                lst.append(thousands[0])
            elif (num % 100) % 10 in [2, 3, 4] and num % 100 not in [12, 13, 14]:
                lst[len(lst) - 1] = dct[(num % 100) % 10][1]
                lst.append(thousands[1])
            elif num != 0:
                lst.append(thousands[2])

        if rank == 3:
            if (num % 10) % 10  == 1 and num % 100 != 11:
                lst.append(millions[0])
            elif (num % 100) % 10 in [2, 3, 4] and num % 100 not in [12, 13, 14]:
                lst.append(millions[1])
            else:
                lst.append(millions[2])
        return " ".join(lst)

    ones = ['один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    tens = ['десять', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
    hundreds = ['сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']
    thousands = ['тысяча', 'тысячи', 'тысяч']
    millions = ['миллион', 'миллиона', 'миллионов']
    teens = ['одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать' ]

    dct = {i + 1: [ones[i]] for i in range(len(ones))}
    dct[1].append('одна')
    dct[2].append('две')
    dct[3].append('три')
    dct[4].append('четыре')
    dct.update({(i + 1) * 10: [tens[i]] for i in range(len(tens))})
    dct.update({(i + 1) * 100: [hundreds[i]] for i in range(len(hundreds))})
    dct.update({(i + 11): [teens[i]] for i in range(len(teens))})
    dct.update({0: ['']})
    #dct

    #number = randint(0, 999999999)
    # Пользователь должен задать rang - число в диапазоне от нуля до которого будут генерироваться числа
    def generate():
        number = randint(0, rang)
        parts = divide_on_three(number)
        if number == 0:
            #print(number)
            return (0,"ноль")
        #print("ноль")
        else:
            l = []
            for i,e in enumerate(parts):
                lst, num = convert_to_words(e)
                #print('lst', lst, num)
                l.append(add_inflections(num, i + 1, lst))
                #print(number)
                #print(result)
                return (number,' '.join(l[::-1]).replace('   ', ' ').replace('  ', ' ').strip())

    #Пользователь должен задать count - сколько чисел ему нужно
    if rang<1 or rang>999999999:
            assertion = 'Пожалуйста выберите число в диапазоне от 1 до 999999999'
            task_text = task.format(assertion)
    else:
        task_text = task[:]
        key_text = task[:]
        for n in range(count):
            number, key = generate()
            task_text = task_text.format(str(number))
            key_text = task_text.format(str(key))
            if n<count-1:
                task_text = task_text+'\n{}'

    # записываем задание и ключи
    fun.writing(task_text, task_name)
    fun.writing_key(key_text, task_name)

    # выводим на сайт
    site_task_text = task_text.replace('\n', '<br>')
    print(site_task_text, "<br><br><br>")
    print("Ответы:<br>")
    site_key_text = key_text.replace('\n', '<br>')
    site_key_text = site_key_text.replace(task,'')
    print(site_key_text)

    show_task_name = str(task_name) +'_show'
    fun.writing(site_task_text,show_task_name )
