from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from .models import *
from cart.models import *
from .forms import *

def home(request):
    categories= Category.objects.all()
    products=Product.objects.all().order_by('price')

    context={
    'categories': categories,
    'products': products
    }
    return render (request, 'home.html', context)

def product_list(request):
    product_list= Product.objects.all()
    filtered_orders= Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products= []
    if filtered_orders.exists():
        user_order= filtered_orders[0]
        user_order_items= user_order.items.all()
        current_order_products= [product.product for product in user_order_items]
    context={
    'product_list': product_list,
    'current_order_products': current_order_products,
    }
    return render(request, "product_list.html", context)

def product_category(request, slug):
    category= Category.objects.get(slug=slug)
    products=Product.objects.all()
    context={
    'category': category,
    'products': products
    }
    return render(request, 'cat_details.html', context)

def user_register(request):
    form=UserRegister()
    if request.method == 'POST':
        form= UserRegister(request.POST)
        if form.is_valid():
            user= form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect ('home' )
    context={
    "form": form,
    }

    return render(request, 'register.html', context)

def user_login(request):
    form= UserLogin()
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password= form.cleaned_data['password']
        auth_user= authenticate(username=username, password=password)
        if auth_user is not None:
            login(request, auth_user)
            messages.success(request, "Welcome Back!")
            return redirect('home')

    context={
    "form": form,
    }
    return render(request, 'login.html', context)

def user_logout(request):
    logout(request)
    return render (request, "logout.html")

def user_profile(request):
    user_profile= Profile.objects.filter(user=request.user).first()
    user_orders= Order.objects.filter(is_ordered=True, owner= user_profile)
    context={
    'user_orders': user_orders
        }
    return render (request, 'profile.html', context)
