from django.urls import path, include
from . import views as views
from django.conf.urls import url
app_name = 'nail'
urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.login, name='login'),
]
