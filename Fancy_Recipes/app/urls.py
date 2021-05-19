from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IngredientListView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/updateProfile/', views.updateProfile, name='updateProfile'),
    path('profile/deleteProfile/', views.deleteProfile, name='deleteProfile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('users/', views.list_users, name='listUsers'),

    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('ingredient/create/', views.create_ingredient, name='ingredient-create'),
    path('ingredient/delete/', views.delete_ingredient, name='ingredient-delete'),
    path('ingredient/list/', IngredientListView.as_view(), name='ingredient-list'),

    path('recipe/add/', views.add_recipe, name='recipe-add'),
    path('recipe/list/', views.list_recipe, name='recipe-list'),
    path('recipe/edit/<int:recipe_id>', views.edit_recipe, name='recipe-edit'),
    path('recipe/delete/<int:recipe_id>', views.recipe_delete, name='recipe-delete'),
    path('recipe/<int:recipe_id>', views.recipe_page, name='recipe_page'),

    path('unit/add/', views.add_unit, name='add_unit'),
    path('unit/delete/', views.delete_unit, name='delete_unit'),
    path('unit/edit/', views.edit_unit, name='edit_unit'),
    path('unitCalculator/', views.unit_calculator, name='unit_calculator'),
    path('unitCalculator/calculate/', views.calculate, name='calculate'),

    path('test/', views.filterRecipes, name='filter'),
]
