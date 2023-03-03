from ast import Try
from http import cookies
from multiprocessing import context
from tkinter.tix import Form
from urllib import request
from django.http import JsonResponse
import json
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.views.generic import ListView
from django.template.loader import render_to_string

def home(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0 ,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'home.html', context)



def about(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0 ,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'about.html', context)


def contact(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems= order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0 ,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
        
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'contact.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)


def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)

def store(request):
	data = cartData(request)
    
    
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
  

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
    
	return JsonResponse('Payment submitted..', safe=False)  

    
def search(request):
    
    q=request.GET['q']
    data=Product.objects.all()
    
    return render(request, 'search.html', {'data':data})


# Search
def search(request):
	q=request.GET['q']
	data=Product.objects.filter(name=q).order_by('-id')
	return render(request,'search.html',{'data':data})
        
   
