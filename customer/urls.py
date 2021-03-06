from django.urls import path
from customer.views import *
urlpatterns = [
    path('reservation/',Reservation,name='reservation'),
    path('account/',Account,name='account'),
    path('logout/', Logout, name='logout'),
    path('address/', address, name='address'),
    path('cart/', Cart, name='cart'),
    path('deleteOrder/<int:Oid>',deleteOrder, name='dOrder'),
    path('deletecartitem/<int:cid>/', deleteCartItem, name='deletecartitem'),
    path('payment/',Payment,name = "payment"),
    path('payment_check/',Payment_check, name = 'payment_check'),
    path('payment_declined/',PaymentDeclined, name = 'payment_declined'),
]
