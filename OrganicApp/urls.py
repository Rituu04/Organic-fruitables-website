from django.urls import path
from .views import *
from . import views

urlpatterns = [
   path('',index,name='index'),
   path('cart/',views.cart_page,name='cart'),
   path('contact/',contact,name='contact'),
   path('shop/',views.shop,name='shop'),
   path('testimonial/',testimonial,name='testimonial'),
   path('checkout/',views.checkout,name='checkout'),
   path('login/',login,name='login'),
   path('register/',register,name='register'),
   path('logout/',logout,name='logout'),
   path('add-to-cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
   path('remove-cart/<int:cid>/', views.remove_cart, name='remove_cart'),
   path('bill/<int:order_id>/', views.bill_page, name='bill_page'),
   path('place-order/', views.place_order, name='place_order'),
   path('search/', views.search, name='search'),
]
