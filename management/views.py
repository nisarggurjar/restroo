from django.shortcuts import render, redirect
from customer.models import Address as AddressModel
from customer.models import Add_to_cart, reservation
from management.models import *
from management.models import Category as ctgmodel
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def HeaderCart(usr):
    cartDish = Add_to_cart.objects.filter(user = usr)
    total = 0
    for i in cartDish:
        total += (i.dish.price) * (i.qty)
    return cartDish, total, len(cartDish)

def About(request):
    team = Team.objects.all()
    if request.user.is_anonymous:
        d = {'team':team}
    else:
        cartDish, total, orderCount = HeaderCart(request.user)
        d = {'team':team, 'cartDish':cartDish, 'total':total, 'orderCount':orderCount }
    return render(request, 'about.html',d)

def Menu(request):
    cat = Category.objects.all()
    dish = Dish.objects.filter(avail = True)
    if request.user.is_anonymous:
        d = {'cat':cat, 'dish':dish}
    else:
        cartDish, total, orderCount = HeaderCart(request.user)
        d = {'cat':cat, 'dish':dish, 'cartDish':cartDish,'orderCount':orderCount, 'total':total}
    return render(request, 'menu.html', d)

def Contact(request):
    d = {}
    if request.user.is_authenticated:
        cartDish, total, orderCount = HeaderCart(request.user)
        d = {'cartDish':cartDish, 'total':total, 'orderCount':orderCount}
    return render(request, 'contact.html',d)

def SinglePage(request, dishid):
    dish = Dish.objects.filter(id = dishid).first()
    d = {}
    if request.POST:
        if not request.user.is_authenticated:
            return redirect('account')
        add = AddressModel.objects.filter(user = request.user)
        data = Add_to_cart.objects.filter(user = request.user, dish = dish).first()
        if add:
            if data:
                Add_to_cart.objects.filter(user = request.user, dish = dish).update(qty = request.POST['qty'])
            else:
                Add_to_cart.objects.create(user = request.user, dish = dish, qty = request.POST['qty'])
        else:
            return redirect('address')  
    if request.user.is_authenticated:
        cartDish, total,orderCount = HeaderCart(request.user)
        d = {'dish':dish, 'cartDish':cartDish,'orderCount':orderCount, 'total':total}
    else:
        d = {'dish':dish}
    return render(request, 'shop_single_full.html', d)

def Orders(request,oid):
    if request.user.is_anonymous:
        return redirect('account')
    dish = Dish.objects.filter(id = oid).first()
    add = AddressModel.objects.filter(user = request.user)
    if add:
        data = Add_to_cart.objects.filter(user = request.user, dish = dish).first()
        if data:
            Add_to_cart.objects.filter(user = request.user, dish = dish).update(qty = data.qty+1)
        else:
            Add_to_cart.objects.create(user = request.user, dish = dish, qty = 1)
    else:
        return redirect('address')
    return redirect('menu')
    

def AdminPanel(request):
    if not request.user.is_staff:
        return redirect('home')
    res = reservation.objects.all()
    orders = Add_to_cart.objects.all()
    if 'delete' in request.POST:
        reservation.objects.get(id = request.POST['delete']).delete()
    if 'confirm' in request.POST:
        reservation.objects.filter(id = request.POST['confirm']).update(confirm = True)
        r = reservation.objects.get(id = request.POST['confirm'])
        sub = 'reservation confirmed at tomato'
        from_mail = settings.EMAIL_HOST_USER
        data = { 'name':r.name, 'guests':r.guests, 'date':r.date, 'time':r.time }
        html = get_template('mail.html').render(data)
        msg = EmailMultiAlternatives(sub, '', from_mail, [r.email])
        msg.attach_alternative(html, 'text/html')
        msg.send()
    if 'deleteOrder' in request.POST:
        Add_to_cart.objects.filter(id = request.POST['deleteOrder']).delete()
    if 'confirmOrder' in request.POST:
        Add_to_cart.objects.filter(id = request.POST['confirmOrder']).update(confirm = True)
    d = {'res':res, 'orders':orders}
    return render(request, 'index2.html',d)

def EditCat(request):
    cat = Category.objects.all()
    d = {'cat':cat}
    if 'delete' in request.POST:
        Category.objects.filter(id = request.POST['delete']).delete()
    if 'addCat' in request.POST:
        Category.objects.create(name = request.POST['name'])
    return render(request, 'editcat.html',d)

def EditDish(request):
    dish = Dish.objects.all()
    cat = Category.objects.all()
    if 'avail' in request.POST:
        Dish.objects.filter(id = request.POST['avail']).update(avail = True)
    if 'unavail' in request.POST:
        Dish.objects.filter(id = request.POST['unavail']).update(avail = False)
    if 'addish' in request.POST:
        data = request.POST
        c = ctgmodel.objects.get(id = int(data['cat']))
        title = data['title']
        mrp = data['mrp']
        price = data['price']
        dis = data['dis']
        img = request.FILES['img']
        img1 = request.FILES['img1']
        img2 = request.FILES['img2']
        Dish.objects.create(cat = c, title = title, price = price, mrp = mrp, dis =dis, img = img, img1 = img1, img2 = img2)
    if 'delete' in request.POST:
        Dish.objects.filter(id = request.POST['delete']).delete()
    d={'cat':cat,'dish':dish}
    return render(request, 'editdish.html',d)

def EditTeam(request):
    team = Team.objects.all()
    if 'delete' in request.POST:
        Team.objects.filter(id = request.POST['delete']).delete()
    if 'addteam' in request.POST:
        data = request.POST
        Team.objects.create(name=data['name'], designation = data['desig'], fb = data['fb'], tw = data['tw'], insta = data['insta'], img = request.FILES['img'])
    d = {'team':team}
    return render(request, 'editteam.html',d)

def error404(request, exception):
    return render(request, '404.html')

def deleteCartItem(request, dishid):
    if request.user.is_anonymous:
        return redirect('account')
    data = Add_to_cart.objects.filter(user = request.user, id = dishid).delete()