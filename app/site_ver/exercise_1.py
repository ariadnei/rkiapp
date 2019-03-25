'''
1. Задание на алфавит: расставить в правильном порядке.
'''

def main():
    import app.site_ver.functions as fun

    task_name = 1
    task = 'Расставьте буквы (1)-(33) в алфавитном порядке.\n\n{}\n{}\n'
    task_1 = 'Расставьте буквы (1)-(33) в алфавитном порядке.'
    site_task = '<pre class="text-task">Расставьте буквы (1)-(33) в алфавитном порядке.<br><br>{}<br>{}</pre>'

    alphabet = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    numbers = [str(i) for i in range(1,34)]


    rand_letters, right_letters = fun.shuffle(alphabet)
    #print(rand_letters)
    #print(right_letters)


    # форматируем тексты задания и ключей
    task_text = task.format('\t'.join(numbers), '\t'.join(rand_letters))
    key_text = task.format('\t'.join([str(i) for i in right_letters]), '\t'.join(alphabet))

    # записываем задание и ключи
    fun.writing(task_text, task_name)
    fun.writing_key(key_text, task_name)

    # выводим на сайт
    site_task_text = site_task.format('\t'.join(numbers), '\t'.join(rand_letters))
    print(site_task_text, "<br><br><br>")
    print("Ответы:<br>")
    site_key_text = '{}<br>{}'.format('\t'.join([str(i) for i in right_letters]), '\t'.join(alphabet))
    print(site_key_text)

    show_task_name = str(task_name) +'_show'
    fun.writing(site_task_text,show_task_name )
