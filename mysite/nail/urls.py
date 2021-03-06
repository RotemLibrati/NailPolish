from django.urls import path, include
from . import views as views
from django.conf.urls import url
app_name = 'nail'
urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('new-user/', views.new_user, name='new-user'),
    path('success/', views.success, name='success'),
    path('<str:username>/new-profile/', views.new_profile, name='new-profile'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('meeting/', views.meeting, name='meeting'),
    path('not-success/', views.not_success, name='not-success'),
    path('pictures/', views.pictures, name='pictures'),
    path('meeting-admin/', views.meeting_admin, name='meeting-admin'),
    path('set-change/', views.set_change, name='set-change'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
]
