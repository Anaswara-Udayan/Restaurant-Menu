from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('menu/',views.menu_view,name='menu'),
    path('order/',views.order_view,name='order'),
    path('order_success/',views.order_success_view,name='order_success')
]

