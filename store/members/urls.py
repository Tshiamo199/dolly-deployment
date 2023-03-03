from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name="home"),
   path('about/',views.about, name='about'),
   path('contact/',views.contact, name ='contact'),
   path('store/', views.store, name="product"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
   path('search/', views.search, name='search'),

   path('update_item/', views.updateItem, name="update_item"),
   path('process_order/', views.processOrder, name="process_order"),
  
]