from django.urls import path
from bandsnap import views

app_name = 'bandsnap'
urlpatterns = [
path('', views.index, name='index'),
path('about/', views.about, name='about'),
path('search/', views.search, name='search'),
path('display-search/', views.display_search, name='display_search'),
path('join_request/', views.join_band, name='join_request'),
path('login/', views.user_login, name='login'),
path('signup/', views.signup, name='signup'),
path('restricted/', views.restricted, name='restricted'),
path('logout/', views.user_logout, name='logout'),
path('profile/', views.user_profile, name='user_profile'),
]