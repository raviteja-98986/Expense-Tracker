from django.urls import path
from . import views
urlpatterns = [
    path('index/',views.index,name='index'),
    path('edit/<int:id>/',views.edit_expense,name='edit'),
    path('delete/<int:id>/',views.delete_expense,name='delete'),
]