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

    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('ingredient/create/', views.create_ingredient, name='ingredient-create'),
    path('ingredient/delete/', views.delete_ingredient, name='ingredient-delete'),
    path('ingredient/list/', IngredientListView.as_view(), name='ingredient-list'),

    path('recipe/add/', views.add_recipe, name='recipe-add'),
    path('recipe/list/', views.list_recipe, name='recipe-list'),
    path('recipe/edit/<int:id>', views.edit_recipe, name='edit-recipe'),
    path('recipe/delete/<int:recipe_id>', views.delete_recipe, name='delete-recipe'),

]
