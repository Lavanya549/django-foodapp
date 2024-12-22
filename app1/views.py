from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from app1.models import *

# Create your views here.

def render_home(request):
    '''messages.success(request, "I know You are Hungry.. I don't let my friends with hungry stomach")'''
    all = Fooditem.objects.all()
    print("Hello")
    if request.method == "POST":
        items = request.POST.get("items")
        print(items)
        print("Hello")
        all = Fooditem.objects.filter(itemtype=items)
        return render(request, "home.html", {"all": all})
    return render(request, "home.html", {"all": all})



@login_required(login_url="userlogin")
def add_cart(request, rid):
    obj = Fooditem.objects.get(id=rid)
    cart_item = Cart(item=obj)
    cart_item.save()
    messages.success(request, f"{cart_item.item.itemname} successfully added to the cart :)")
    return redirect("home")



def render_item_reg(request):
    if request.method == "POST":
        itempic = request.FILES.get("itempic")
        itemname = request.POST.get("itemname")
        price = request.POST.get("price")
        itemtype = request.POST.get("itemtype")
        rating = request.POST.get("rating")
        availability = request.POST.get("availability")
        obj = Fooditem(itempic=itempic, itemname=itemname, price=price, itemtype=itemtype, rating=rating, availability=availability)
        obj.save()
        messages.success(request, f"{itemname} successfully added to the menu :) please add more")
        return redirect("itemreg")
    return render(request, "item_register.html")



def render_user_login(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        pword = request.POST.get("pword")
        obj = authenticate(username=uname, password=pword)
        if obj:
            login(request, obj)
            messages.success(request, "You are successfully logged in")
            return redirect("home")
        messages.error(request, "Please enter valid credentials")
        return redirect("userlogin")
    return render(request, "user_login.html")



def render_user_reg(request):
    return render(request, "user_register.html")



def render_single(request, rid):
    obj = Fooditem.objects.get(id=rid)
    return render(request, "single.html", {"obj": obj})



def logout_user(request):
    logout(request)
    return redirect("userlogin")



@login_required(login_url="userlogin")
def render_show_cart(request):
    all = Cart.objects.all()
    total = 0
    for i in all:
        total += i.item.price
    return render(request, "cart.html", {"all": all, "total": total})



def empty_cart(request):
    all = Cart.objects.all()
    for i in all:
        i.delete()
    return redirect("showcart")


@login_required(login_url="userlogin")
def remove_item(request, rid):
    obj = Cart.objects.get(id=rid)
    obj.delete()
    return redirect("showcart")



@login_required(login_url="userlogin")
def render_order(request):
    if request.method == "POST":
        addr = request.POST.get("addr")
        phno = request.POST.get("phno")
        order_items = Cart.objects.all()
        for i in order_items:
            obj = Order(usern=request.user, addr=addr, phno=phno, items=i)
            obj.save()
        messages.success(request, "Order placed successfully")
        return redirect("ordered")
    return render(request, "order.html")



@login_required(login_url="userlogin")
def render_ordered(request):
    total = 0
    all = Order.objects.all()
    obj = all[0]
    for i in all:
        total += i.items.item.price
    print(all)
    return render(request, "ordered.html", {"all": all, "total": total, "obj": obj})