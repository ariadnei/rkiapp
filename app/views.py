from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from requests import post
# from xml.etree import ElementTree as ET
# from xml.etree. ElementTree import ParseError

num = ''
def main_view(request):
    displaying_home = True
    return render(request, r'app/index.html', {'displaying_home':displaying_home})

def display_example(request):
    displaying_examples = True
    return render(request, r'app/index.html', {'displaying_examples':displaying_examples})

from django import forms

class UploadFileForm(forms.Form):
    CHOICES = (('ex1', 'Упражнение 1'),('ex2', 'Упражнение 2'),('ex3', 'Упражнение 3'), ('ex4', 'Упражнение 4'), ('ex5', 'Упражнение 5'), ('ex6', 'Упражнение 6'), ('ex7', 'Упражнение 7'), ('ex8', 'Упражнение 8'), ('ex9', 'Упражнение 9'))
    exc = forms.ChoiceField(choices=CHOICES, label='Выберите упражнение')
    LEVELS = (('A1', 'A1'),('A2', 'A2'),('B1', 'B1'),('B2', 'B2'),)
    lev = forms.ChoiceField(choices=LEVELS, label='Выберите уровень', required=False)
    coe_imp = forms.FloatField(label='Выберите коеффициент значимых слов', required=False)
    to_gen = forms.IntegerField(label='Выберите до какого числа генерировать', required=False)
    num_gen = forms.IntegerField(label='Выберите сколько чисел генерировать', required=False)
    #title = forms.CharField(max_length=50)
    file  = forms.FileField(label='Загрузите файл с текстом в формате .txt', required=False)
    #exc.widget.attrs.update({'class': 'special'})

from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.shortcuts import render_to_response

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

import app.site_ver.exercise_1 as exc1
import app.site_ver.exercise_2 as exc2
import app.site_ver.exercise_3 as exc3
import app.site_ver.exercise_4 as exc4
import app.site_ver.exercise_5 as exc5
import app.site_ver.exercise_6 as exc6
import app.site_ver.exercise_7 as exc7
import app.site_ver.exercise_8 as exc8
import app.site_ver.exercise_9 as exc9

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            num_exc = form.cleaned_data['exc']
            num_lev = form.cleaned_data['lev']
            num_c = form.cleaned_data['coe_imp']
            num_to_gen = form.cleaned_data['to_gen']
            num_num_gen = form.cleaned_data['num_gen']
            handle_uploaded_file(request.FILES['file'])
            if num_exc == 'ex1':
                request.session['num'] = 1
                exc1.main()
            if num_exc == 'ex2':
                request.session['num'] = 2
                exc2.main()
            if num_exc == 'ex3':
                print('num_c', num_c)
                request.session['num'] = 3
                exc3.main(num_lev, num_c)
            if num_exc == 'ex4':
                request.session['num'] = 4
                exc4.main(num_lev, num_c)
            if num_exc == 'ex5':
                request.session['num'] = 5
                exc5.main(num_lev)
            if num_exc == 'ex6':
                request.session['num'] = 6
                exc6.main()
            if num_exc == 'ex7':
                request.session['num'] = 7
                exc7.main(num_lev)
            if num_exc == 'ex8':
                request.session['num'] = 8
                exc8.main(num_lev)
            if num_exc == 'ex9':
                request.session['num'] = 9
                exc9.main(num_to_gen, num_num_gen)
            return HttpResponseRedirect('/upload/success')
    else:
        form = UploadFileForm()
        displaying_form = True

    return render(request, r'app/index.html', {'form': form, 'displaying_form':displaying_form})

def handle_uploaded_file(f):
    #title_dest = open('app/uploads/files/title.txt', 'wb+')
    destination = open('app/uploads/files/text.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

    destination.close()

def show_res(request):
    num = request.session.get('num')
    task_path = 'app/uploads/to_download/task_'+str(num)+'_show'+ '.txt'
    text = open(task_path).read()
    download_task = True
    return render(request, r'app/index.html', {'task': text, 'download_task':download_task})
    #return HttpResponse("<p>{0}</p>".format(text))

from wsgiref.util import FileWrapper


# def download_task(request):
#     filename = 'app/uploads/to_download/task.txt'
#     content = FileWrapper(filename)
#     response = HttpResponse(content, content_type='text/plain')
#     response['Content-Length'] = os.path.getsize(filename)
#     response['Content-Disposition'] = 'attachment; filename=%s' % 'generated_task.txt'
#     return response


def download_task(request):
    num = request.session.get('num')
    task_path = 'app/uploads/to_download/task_' + str(num) + '.txt'
    task_download_name = 'attachment;filename=task_' + str(num) + '.txt'
    with open(task_path, 'rb') as task:
    	response = HttpResponse(task.read())
    	response['content_type'] = 'text/plain'
    	response['Content-Disposition'] = task_download_name
    	return response

def download_answer(request):
    num = request.session.get('num')
    ans_path = 'app/uploads/to_download/answ.txt'
    answ_download_name = 'attachment;filename=answers_' + str(num) + '.txt'
    with open(ans_path, 'rb') as task:
    	response = HttpResponse(task.read())
    	response['content_type'] = 'text/plain'
    	response['Content-Disposition'] = answ_download_name
    	return response
# def download_pdf(request):
#     filename = 'whatever_in_absolute_path__or_not.pdf'
#     content = FileWrapper(filename)
#     response = HttpResponse(content, content_type='application/pdf')
#     response['Content-Length'] = os.path.getsize(filename)
#     response['Content-Disposition'] = 'attachment; filename=%s' % 'whatever_name_will_appear_in_download.pdf'
#     return response


# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/upload/thanks/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, r'app/index.html', {'form': form})
#
# import json
#
# def set_var(request):
#     #res = json.loads(request);
#     return render(request, r'app/index.html', {'vars': request.data})
#
# from django.http import HttpResponseRedirect
# def processForm(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#
#     return render(request, 'index.html', {'form': form})
