from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.upload_file, name = 'upload-file'),
    path('success/', views.show_res, name = 'show_res'),
    #path('success/url/', views.handle_uploaded_file, name = 'handle-file'),

    #path('download/processing', views.processForm, name = 'process_form')
    #path('', views.MainSearchView(), name = 'main-view'),
    #path('process/', views.processSpeech, name = 'process_speech')
    #path('autocomplete/', views.autocomplete)
]
