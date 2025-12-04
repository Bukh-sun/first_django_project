from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # главная страница блога
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # страница поста
    path('category/<int:category_id>/', views.category_list, name='category_list'),  # посты категории
]