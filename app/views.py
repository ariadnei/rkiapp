from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from requests import post
# from xml.etree import ElementTree as ET
# from xml.etree. ElementTree import ParseError

def main_view(request):
    displaying_home = True
    return render(request, r'app/index.html', {'displaying_home':displaying_home})

def display_example(request):
    displaying_examples = True
    return render(request, r'app/index.html', {'displaying_examples':displaying_examples})

from django import forms

class UploadFileForm(forms.Form):
    CHOICES = (('ex1', 'Упражнение 1'),('ex2', 'Упражнение 2'),('ex3', 'Упражнение 3'),)
    exc = forms.ChoiceField(choices=CHOICES, label='Выберите упражнение')
    #title = forms.CharField(max_length=50)
    file  = forms.FileField(label='Загрузите файл с текстом в формате .txt')
    #exc.widget.attrs.update({'class': 'special'})

from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.shortcuts import render_to_response

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file

import app.exc.exercise_1 as exc1
import app.exc.exercise_2 as exc2
import app.exc.exercise_3 as exc3

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            num_exc = form.cleaned_data['exc']
            handle_uploaded_file(request.FILES['file'])
            if num_exc == 'ex1':
                exc1.main()
            if num_exc == 'ex2':
                exc2.main()
            if num_exc == 'ex3':
                exc3.main()
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
    text = open('app/uploads/to_download/task.txt').read()
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
    with open('app/uploads/to_download/task.txt', 'rb') as task:
    	response = HttpResponse(task.read())
    	response['content_type'] = 'text/plain'
    	response['Content-Disposition'] = 'attachment;filename=task.txt'
    	return response

def download_answer(request):
    with open('app/uploads/to_download/answ.txt', 'rb') as task:
    	response = HttpResponse(task.read())
    	response['content_type'] = 'text/plain'
    	response['Content-Disposition'] = 'attachment;filename=answers.txt'
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
