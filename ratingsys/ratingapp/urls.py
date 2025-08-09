from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='ratingapp/login.html'), name='login'),
    path('index/', views.index, name='index'),
    path('add_student/', views.add_student_view, name='add_student'),
    path('add_result/', views.add_result_view, name='add_result'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
  ] 