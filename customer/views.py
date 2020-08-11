from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from customer.models import Address as AddressModel
from customer.models import Add_to_cart, reservation
from management.models import *
from django.contrib.auth.models import User
import requests
import json

def HeaderCart(usr):
    cartDish = Add_to_cart.objects.filter(user = usr)
    total = 0
    for i in cartDish:
        total += (i.dish.price) * (i.qty)
    return cartDish, total

def Home(request):
    if request.user.is_staff:
        return redirect('AdminPanel')
    cat = Category.objects.all()
    dishes = Dish.objects.filter(avail = True)
    if request.user.is_anonymous:
        d = {'cat':cat, 'dishes':dishes}
    else:
        cartDish, total = HeaderCart(request.user)
        d = {'cat':cat, 'dishes':dishes, 'cartDish':cartDish, 'total':total}
    return render(request, 'index.html',d)

def Reservation(request):
    msg = False
    if request.POST:
        if request.user.is_anonymous:
            return redirect('account')
        date = request.POST['date']
        time = request.POST['time']
        name = request.user.username
        email = request.user.email
        guests = request.POST['guests']
        mob = request.POST['mob']
        reservation.objects.create(user = request.user,date = date, time = time, name = name, email = email, guests = guests, mob = mob)
        msg = True
    if request.user.is_anonymous:
       d = {'msg':msg}
    else:
        cartDish, total = HeaderCart(request.user)
        d = {'msg':msg, 'cartDish':cartDish, 'total':total}
    return render(request,'reservation.html',d)

def Account(request):
    errorL = False
    errorEmail = False
    errorPass = False
    errorUser = False
    if 'login' in request.POST:
        un = request.POST['un']
        pwd = request.POST['pwd']
        user = authenticate(username = un, password = pwd)
        if user:
            login(request, user)
            if request.user.is_staff:
                return redirect('AdminPanel')
            return redirect('home')
        else:
            errorL = True
    if 'signup' in request.POST:
        email = request.POST['e']
        ev = json.loads(requests.get('https://api.trumail.io/v2/lookups/json?email=' + email).text)
        un = request.POST['un']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        check = User.objects.filter(username = un)
        if ev['deliverable'] is not True:
            errorEmail = True
        elif pwd1 != pwd2:
            errorPass = True
        elif check:
            errorUser = True
        else:
            User.objects.create_user(username = un, email = email, password = pwd1, is_staff = False)
            user = authenticate(username = un, password = pwd1)
            login(request,user)
            return redirect('home')
    d = {'errorL':errorL,'errorPass':errorPass, 'errorUser':errorUser, 'errorEmail':errorEmail}
    return render(request, 'account.html',d)

def address(request):
    error = False
    errorMob = False
    if request.user.is_anonymous:
        return redirect('account')
    if request.POST:
        user = request.user
        hn = request.POST['hn']
        area = request.POST['area']
        lm = request.POST['lm']
        pin = request.POST['pin']
        city = request.POST['city']
        mob = request.POST['mob']
        PinResult = requests.get('https://api.postalpincode.in/pincode/'+ str(pin))
        pintext = PinResult.text
        PinJson = json.loads(pintext)
        pinStatus = PinJson[0]['Status']
        mobresult = json.loads(requests.get('http://apilayer.net/api/validate?access_key=5f03710ab66ec4d216ca50bd61587d71&number=' + str(mob)+ '&country_code=IN&format=1').text)
        if mobresult['valid'] and mobresult['country_code'] == 'IN' and mobresult['line_type'] is not "special_services":
            if pinStatus == "Success" :
                noOfDiv = int(PinJson[0]['Message'][27:])
                t = 0
                names = ''
                for i in range(noOfDiv):
                    if PinJson[0]['PostOffice'][i]['DeliveryStatus'] == "Delivery":
                        t+=1
                if (t>0):
                    dist = PinJson[0]['PostOffice'][0]['District']
                    state = PinJson[0]['PostOffice'][0]['State']
                    AddressModel.objects.create(user = request.user,HouseNum = hn, area=area,city=city,district= dist,state = state, pin = pin,mobile = mob, landmark = lm)
                    return redirect('menu')
                else:
                    error = True
            else:
                error = True
        else:
            errorMob = True
    return render(request,'address.html',{'error':error, 'errorMob':errorMob})

def Logout(request):
    logout(request)
    return redirect('account')

def Cart(request):
    cartDish, total = HeaderCart(request.user)
    d = {'cartDish':cartDish,'total':total}
    return render(request, 'shop_cart.html', d)

def deleteOrder(request, Oid):
    Add_to_cart.objects.get(id = Oid).delete()
    return redirect('cart')

def deleteCartItem(request, cid):
    if request.user.is_anonymous:
        return redirect('account')
    data = Add_to_cart.objects.filter(user = request.user, id = cid).delete()
    return redirect('menu')