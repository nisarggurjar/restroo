from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from customer.models import Address as AddressModel
from customer.models import Add_to_cart, reservation, user_details, Payment_ids
from management.models import *
from django.contrib.auth.models import User
import requests
import json

def HeaderCart(usr):
    cartDish = Add_to_cart.objects.filter(user = usr, confirm = False)
    total = 0
    for i in cartDish:
        total += (i.dish.price) * (i.qty)
    return cartDish, total, len(cartDish)

def Home(request):
    if request.user.is_staff:
        return redirect('AdminPanel')
    cat = Category.objects.all()
    dishes = Dish.objects.filter(avail = True)
    if request.user.is_anonymous:
        d = {'cat':cat, 'dishes':dishes}
    else:
        cartDish, total, orderCount = HeaderCart(request.user)
        d = {'cat':cat, 'dishes':dishes,'orderCount':orderCount, 'cartDish':cartDish, 'total':total}
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
        cartDish, total, orderCount = HeaderCart(request.user)
        d = {'msg':msg, 'cartDish':cartDish, 'orderCount':orderCount, 'total':total}
    return render(request,'reservation.html',d)

def Account(request):
    errorL = False
    errorEmail = False
    errorMob = False
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
        mob = request.POST['mob']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        mv = json.loads(requests.get('http://apilayer.net/api/validate?access_key=b4385e3165e0c8d4fd2ee501d953de30&number='+ mob +'&country_code=IN&format=1').text)
        check = User.objects.filter(username = un)
        if ev['deliverable'] is not True:
            errorEmail = True
        elif pwd1 != pwd2:
            errorPass = True
        elif check:
            errorUser = True
        elif mv['valid'] is not True and mv['country_code'] is not 'IN' and mv['line_type'] is "special_services":
            errorMob = True
        else:
            User.objects.create_user(username = un, email = email, password = pwd1, is_staff = False)
            user = authenticate(username = un, password = pwd1)
            login(request,user)
            user_details.objects.create(user = request.user, mob = mob)
            return redirect('home')
    d = {'errorL':errorL,'errorPass':errorPass, 'errorUser':errorUser, 'errorEmail':errorEmail, 'errorMob':errorMob}
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
    cartDish, total, orderCount = HeaderCart(request.user)
    d = {'cartDish':cartDish, 'orderCount':orderCount, 'total':total}
    return render(request, 'shop_cart.html', d)

def deleteOrder(request, Oid):
    Add_to_cart.objects.get(id = Oid).delete()
    return redirect('cart')

def deleteCartItem(request, cid):
    if request.user.is_anonymous:
        return redirect('account')
    data = Add_to_cart.objects.filter(user = request.user, id = cid).delete()
    return redirect('menu')

headers = {"X-Api-Key": "3bec9da8d186f2caca726f756252f5c6",
           "X-Auth-Token": "c37cf15ee05894ccc423d642d5928923"}

def PaymentDeclined(request):
    if request.user.is_anonymous:
        return render(request,'paymentError.html')
    else:
        Cartdish, total, orderCount = HeaderCart(request.user)
        return render(request,'paymentError.html', { 'cartDish':cartDish, 'orderCount':orderCount, 'total':total})

def Payment(request):
    Cartdish, total, orderCount = HeaderCart(request.user)
    #product = Product.objects.filter(id = pid).first()
    #user = User_detail.objects.filter(user = request.user).first()
    mob = user_details.objects.get(user=request.user).mob
    purp = str()
    purp = "Payment for Food"
    payload = {
        "purpose":purp,
        "amount":total,
        "buyer_name":str(request.user),
        "email":str(request.user.email),
        "phone":mob,
        "send_email":True,
        "send_sms":True,
        "redirect_url":"http://127.0.0.1:8000/customers/payment_check/"
    }
    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/",
                            data=payload,headers=headers)
    print(response)
    y = response.text
    d = json.loads(y)
    a = d['payment_request']['longurl']
    i = d['payment_request']['id']
    Payment_ids.objects.create(ids = i,user = request.user)
    return redirect(a)

def Payment_check(request):
    pay = False
    i = Payment_ids.objects.filter(user = request.user).first()
    ii = i.ids
    response = requests.get("https://www.instamojo.com/api/1.1/payment-requests/"+str(ii)+'/',
                            headers=headers)
    y = response.text
    b = json.loads(y)
    print(b)
    status = b['payment_request']['status']
    if status=="Completed":
        pay = True
        Cartdish, total, orderCount = HeaderCart(request.user)
        Add_to_cart.objects.filter(user = request.user).update(confirm = True)
        d = {'total':total, 'Cartdish':Cartdish, 'pay':pay, 'orderCount':orderCount}
        return render(request, 'shop_cart.html',d)
    else:
        return redirect('payment_declined')