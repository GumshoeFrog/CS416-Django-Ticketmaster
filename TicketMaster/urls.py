from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name='home'),
path('', views.index, name='index'),
path('add', views.list_add, name='list_add'),
path('save', views.list_save, name='list_save'),
path('update/<str:id> ', views.list_update, name='list_update'),
path('delete/<str:id>', views.list_delete, name='list_delete'),

# path('beta/', views.beta, name='beta'),
]