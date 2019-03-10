from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main_view, name = 'main-view'),
    path('upload/', views.upload_file, name = 'upload-file'),
    path('example/', views.display_example, name = 'display-example'),
    path('upload/success', views.show_res, name = 'show-res'),
    path('upload/download_generated_task/', views.download_task, name = 'download-task'),
    path('upload/download_generated_answer/', views.download_answer, name = 'download-answer'),

    #path('success/url/', views.handle_uploaded_file, name = 'handle-file'),

    #path('download/processing', views.processForm, name = 'process_form')
    #path('', views.MainSearchView(), name = 'main-view'),
    #path('process/', views.processSpeech, name = 'process_speech')
    #path('autocomplete/', views.autocomplete)
]
