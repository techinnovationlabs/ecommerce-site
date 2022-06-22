from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.views import View
from .models import Product
from .models import Order
from .models import OrderItem
from .models import Payment
from .models import Customer
from django.db.models import Sum
from django.shortcuts import render, redirect
import uuid


def homePage(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect(request.META['HTTP_REFERER'])
        return redirect('home')
    else:
        # products = None
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category=category_id)

        else:
            products = Product.objects.all()
        context = {'products': products, 'categories': categories}
        return render(request, 'ecommerce_app/home.html', context)


def login(request):
    if request.method == "GET":
        return render(request, 'ecommerce_app/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_msg = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                request.session['first_name'] = customer.first_name
                return redirect("home")
            else:
                error_msg = "Email or Password is incorrect."
        else:
            error_msg = "Email or Password is incorrect."
        return render(request, 'ecommerce_app/login.html', {'error_msg': error_msg})


def validateCustomer(customer):
    err_msg = None
    if not customer.first_name:
        err_msg = "First Name Required."
    elif len(customer.first_name) < 3:
        err_msg = "First Name must be 3 characters long."
    elif not customer.last_name:
        err_msg = "Last Name Required."
    elif len(customer.last_name) < 3:
        err_msg = "Last Name must be 3 characters long."
    elif not customer.phone:
        err_msg = "Phone is Required."
    elif len(customer.phone) < 10:
        err_msg = "Phone Number must be 10 characters long."
    elif not customer.email:
        err_msg = "Email is Required."
    elif customer.does_exits():
        err_msg = "User with this email address already registered."
        return err_msg


def registerCustomer(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    password = request.POST.get('password')

    values = {
        'firstname': first_name,
        'lastname': last_name,
        'phone': phone,
        'email': email,
    }
    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    err_msg = None
    err_msg = validateCustomer(customer)
    if not err_msg:
        customer.password = make_password(customer.password)
        customer.save()
        return redirect('home')
    else:
        return render(request, 'ecommerce_app/signup.html', {'error_msg': err_msg, 'values': values})


def signup(request):
    if request.method == 'GET':
        return render(request, 'ecommerce_app/signup.html')
    else:
        return registerCustomer(request)


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        print(ids)
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'ecommerce_app/cart.html', {'products': products})


# payment with orderdetails
def payment(request):
    ids = list(request.session.get('cart').keys())
    products = Product.get_products_by_id(ids)
    print(products)
    return render(request, 'ecommerce_app/payment.html', {'products': products})


# orders
class CheckOut(View):
    def post(self, request):
        city = request.POST.get('city')
        country = request.POST.get('country')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        print(city, country, address, phone, customer, cart)
        # for product in products:
        #     print(cart.get(str(product.id)))
        payment = Payment(customer=Customer(id=customer),
                          city=city,
                          country=country,
                          address=address,
                          phone=phone)
        payment.save()

        print('payment', payment)
        if payment:
            order = Order(customer=Customer(id=customer))
            order.save()
            saverecord = order
            print("saverecord:", saverecord)

            if saverecord:
                products = Product.get_products_by_id(list(cart.keys()))
                cart = request.session.get('cart')
                customer = request.session.get('customer')
                # print(cart, products)

            for product in products:
                # print(cart.get(str(product.id)))
                orderitem = OrderItem(customer=Customer(id=customer),
                                      product=product,
                                      order=saverecord,
                                      price=product.price,
                                      total=product.price * cart.get(str(product.id)),
                                      quantity=cart.get(str(product.id)))
                orderitem.save()
                h = str(saverecord)
                token = uuid.UUID(h)

                # token = uuid.(saverecord)
                orderitems = OrderItem.objects.filter(order=saverecord)
            total_amount = orderitems.aggregate(Sum('total'))['total__sum']
            print("total = ", total_amount)
            order = Order.objects.filter(id=token).update(total_amount=total_amount)
            # order.save()

            request.session['cart'] = {}
            return redirect('cart')


def orders(request):
    orders = Order.objects.all()
    return render(request, 'ecommerce_app/orders.html', {'orders': orders})


def orderview(request, order_id):
    orderitems = OrderItem.objects.filter(order=order_id)
    print('orderitems:', orderitems)
    return render(request, 'ecommerce_app/orderview.html', {'orderitems': orderitems})
