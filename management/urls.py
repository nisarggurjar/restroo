from django.urls import path
from .views import *

urlpatterns = [
    path('about/',About, name='about'),
    path('menu/', Menu, name='menu'),
    path('contact', Contact, name='contact'),
    path('dish/<int:dishid>',SinglePage, name='dish'),
    path('AdminPanel/', AdminPanel, name='AdminPanel'),
    path('editCat/',EditCat, name='editcat'),
    path('editdish/', EditDish, name='editdish'),
    path('editteam/', EditTeam, name='editteam'),
    path('order/<int:oid>/', Orders, name='order')
]
