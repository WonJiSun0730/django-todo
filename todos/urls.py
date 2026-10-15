from django.urls import path
from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.todo_list, name='list'),
    path('new/', views.todo_edit, name='create'),
    path('<int:pk>/edit/', views.todo_edit, name='update'),
    path('<int:pk>/delete/', views.todo_delete, name='delete'),
    path('<int:pk>/complete/', views.todo_complete, name='complete'),
]
