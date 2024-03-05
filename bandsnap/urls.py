from django.urls import path
from bandsnap import views

app_name = 'bandsnap'
urlpatterns = [
path('', views.index, name='index'),
]