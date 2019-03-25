'''
2. Разбить текст на абзацы, перемешать, предложить расположить в правильном порядке.
'''

def main():
    import app.exc.functions as fun

    task_name = 2
    task = 'Расставьте абзацы (1)-({}) в правильном порядке, чтобы получить текст.\n\n{}'

    text = fun.reading('text')
    #print(text)

    # делим текст на абазы -- достаточно так
    paragraphs = text.split('\n')
    #print(len(paragraphs))
    #print(paragraphs)

    # перемешиваем абзацы
    rand_paragraphs, right_paragraphs = fun.shuffle(paragraphs)

    # в строку записываем пронумерованный список абзацев
    task_text = ''
    for i, p in enumerate(rand_paragraphs):
        task_text += '{}) {}\n'.format(i+1, p)
    task_text = task_text[:-1]

    # создаём строку с пронумерованными ключами
    keys = fun.list_key(right_paragraphs)

    #print(task_text)
    #print(right_paragraphs)

    # форматируем тексты задания и ключей
    task_text = task.format(len(rand_paragraphs), task_text)
    key_text = task.format(len(rand_paragraphs), keys)

    # записываем задание и ключи
    fun.writing(task_text, task_name)
    fun.writing_key(key_text, task_name)

    # выводим на сайт
    site_task_text = task_text.replace('\n', '<br>')
    print(site_task_text, "<br><br><br>")
    print("Ответы:<br>")
    site_key_text = keys.replace('\n', '<br>')
    print(site_key_text)