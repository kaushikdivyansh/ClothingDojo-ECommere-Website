from django.shortcuts import render, HttpResponse, redirect
from apps.commerce.models import *
from django.conf import settings
import stripe
from decimal import Decimal


#Products page
def products(request):
    #user below is manually entered in for now until linked with platform login
    user = User.objects.get(id=1)
    products = Product.objects.all()
    sizes = Size.objects.all()
    request.session['id'] = user.id

    #determines if logged in user has selected their free shirt. Displays options if false.
    if user.free == True:
        data = {
            'user':user,
            'product':products,
            'size':sizes,
            'free': True
        }
    else:
        data = {
            'user':user,
            'product':products,
            'size':sizes,
            'free': False
        }

    return render(request, 'commerce/products.html', data)


#Cart page
def checkout(request):
    cart = Cart.objects.filter(user=request.session['id'])
    product = Product.objects.all()
    size = Size.objects.all()
    purchase = Purchase.objects.filter(user=request.session['id'])

    #calculates the total amount of values in your cart
    total = 0
    for i in cart:
        total += i.price

    order_data = []
    order_info = []

    #Used for the Ordered items section in your cart. Loops through orders purchased by the user
    #and organizes them for easy display.
    init = 0
    for i in purchase:
        instance = {
            'id' : i.order.id,
            'quantity' : i.quantity,
            'product' : Purchase.objects.get(id=i.id).product.description,
            'size' : Purchase.objects.get(id=i.id).size.size,
            'price' : Purchase.objects.get(id=i.id).product.price,
            'order_total' : Purchase.objects.get(id=i.id).product.price * i.quantity
        }

        if i.order_id != init:
            info = {
                'id': i.order_id,
                'created_at' : i.created_at,
                'locked' : i.order.locked,
            }
            init = i.order_id
            order_info.append(info)

        order_data.append(instance)

    data = {
        'cart':cart,
        'product':product,
        'size':size,
        'purchase' : purchase,
        'total' : total,
        'order_data' : order_data,
        'order_info' : order_info
    }
    return render(request, 'commerce/checkout.html', data)

#Admin page
def admin(request):
    purchase = Purchase.objects.all()
    final_data = []
    cancels = Cancellation.objects.all()
    cancel_data = []

    #Creates the data table to display all purchases
    for i in purchase:
        instance = {
            'id': i.order.id,
            'quantity' : i.quantity,
            'created_at' : i.created_at,
            'city' : Purchase.objects.get(id=i.id).location.city,
            'state' : Purchase.objects.get(id=i.id).location.state,
            'product' : Purchase.objects.get(id=i.id).product.description,
            'size' : Purchase.objects.get(id=i.id).size.size,
            'user' : Purchase.objects.get(id=i.id).user.email
        }
        final_data.append(instance)

    #Creates the CSV file for emailing all users
    address = ''
    users = User.objects.all()
    for i in users:
        address += i.email +','

    address = address[:-1]

    #Creates the table of all cancellation requests
    for i in cancels:
        cancel_instance = {
            'id' : i.id,
            'order_date' : i.order_created_at,
            'cancel_date' : i.created_at,
            'user' : i.user
        }
        cancel_data.append(cancel_instance)

    data = {
        'address': address,
        'final_data' : final_data,
        'cancel_data' : cancel_data
    }

    return render(request, 'commerce/admin.html', data)

#Adds items to your cart
def cart(request, num):
    quantity = int(request.POST[num + '_quantity'])
    #Prevents users from adding negative amounts of items to their cart
    if quantity <=0:
        return redirect('/')

    product = Product.objects.get(id=num)
    size = Size.objects.get(id=request.POST[num +'_size'])
    user = User.objects.get(id=request.session['id'])
    location = user.location
    location = location.id
    price = product.price * quantity
    location = Location.objects.get(id=location)

    #Creates the actual cart item
    Cart.objects.create(quantity=quantity, location=location, product=product, user=user, size=size, price=price)
    return redirect('/')

#Update items in your cart
def update(request, num):
    newsize = request.POST[num+'_size']
    newsize = Size.objects.get(id=newsize)
    newquantity = request.POST[num+'_quantity']
    cart_item = Cart.objects.get(id=num)
    product = Product.objects.get(id=cart_item.product_id)
    price = product.price
    cart_item.quantity = newquantity
    cart_item.size = newsize
    cart_item.price = Decimal(newquantity) * price
    cart_item.save()
    return redirect('/checkout')

#Remove items from your cart
def remove(request, num):
    cart_item = Cart.objects.get(id=num)
    cart_item.delete()
    return redirect('/checkout')

#Loops through items in your cart, creates an Order for the user, and creates a Purchase for each
#item in your cart, linking them to the Order
def purchase(request):
    cart = Cart.objects.filter(user=request.session['id'])
    user = User.objects.get(id= request.session['id'])
    x = Order.objects.create(user=user, locked=False, total=0)
    order_total = 0

    for i in cart:
        Purchase.objects.create(quantity = i.quantity, location=i.location, order=x, product=i.product, size=i.size, user=user, total=i.quantity * i.product.price)
        remove = Cart.objects.get(id=i.id)
        remove.delete()
        order_total += i.quantity * i.product.price

    x.total = order_total
    x.save()

    stripe.api_key = 'sk_live_U5o0zI3ysKOdgJaFrKc55DyV'
    token = request.POST['stripeToken']

    #Creates the Stripe charge
    # customer = stripe.Charge.create(
    #     amount = 199,
    #     currency = 'USD',
    #     description = 'charge',
    #     source = token
    # )
    return redirect('/checkout')

#Creates a purchase for the User's free t-shirt
def free(request):
    user = User.objects.get(id= request.session['id'])
    product = Product.objects.get(id=1)
    x = Order.objects.create(user = user, locked=False, total=product.price)
    size = request.POST['size']
    size = Size.objects.get(id=size)
    Purchase.objects.create(quantity = 1, location=user.location, order=x, product=product, size=size, user=user, total=product.price)
    user.free=True
    user.save()
    return redirect('/')

#If the order is unlocked, deletes the Purchase and Order while also creating a Cancellation request
#in the Cancellation table, allowing you to go to Stripe and locate the correct charge, and refund it
def cancel(request, num):
    purchase = Purchase.objects.filter(order=num)
    order = Order.objects.get(id=num)
    user = User.objects.get(id=request.session['id'])
    Cancellation.objects.create(order_created_at=order.created_at, user=user)
    for i in purchase:
        i.delete()

    order.delete()

    return redirect('/checkout')

#Allows the admin to unlock the current database of Orders, allowing users to cancel orders
def unlock(request):
    order = Order.objects.all()
    for i in order:
        i.locked = False
        i.save()
    return redirect('/admin')

#Allows the admin to lock the current database of Orders, preventing users from cancelling orders
def lock(request):
    order = Order.objects.all()
    for i in order:
        i.locked = True
        i.save()
    return redirect('/admin')

#Admin products page
def viewproduct(request):
    products = Product.objects.all()
    return render(request, 'commerce/viewproduct.html', {'products': products})

#Updates the edited product
def update_product(request, num):
    product = Product.objects.get(id=num)
    product.description = request.POST['description']
    product.price = Decimal(request.POST['price'])
    product.image = request.POST['image']
    product.save()
    return redirect('/viewproduct')

#Adds the product to the database
def add_product(request):
    Product.objects.create(description = request.POST['description'], price = Decimal(request.POST['price']), image = request.POST['image'])
    return redirect('/viewproduct')

#Removes the product from the database
def remove_product(request,num):
    product = Product.objects.get(id=num)
    product.delete()
    return redirect('/viewproduct')

def faq(request):
    return render(request, "commerce/FAQ.html")

def tos(request):
    return render(request, "commerce/tos.html")
