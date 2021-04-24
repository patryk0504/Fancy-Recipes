from django.urls import path
from .views import IngredientListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('ingredient/create/', views.create_ingredient, name='ingredient-create'),
    path('ingredient/delete/', views.delete_ingredient, name='ingredient-delete'),
    path('ingredient/list/', IngredientListView.as_view(), name='ingredient-list')
]
