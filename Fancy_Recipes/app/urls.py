from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IngredientListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name = "logout"),
    path('ingredient/create/', views.create_ingredient, name='ingredient-create'),
    path('ingredient/delete/', views.delete_ingredient, name='ingredient-delete'),
    path('ingredient/list/', IngredientListView.as_view(), name='ingredient-list')
]
