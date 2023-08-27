# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from inventory.forms import UserRegistry, ProductForm, OrderForm
from inventory.models import Product, Order


@login_required
def index(request):
    # Retrieve orders for the current user
    orders_user = Order.objects.all()

    # Retrieve the first two users
    users = User.objects.all()[:4]

    # Retrieve the first two orders
    orders_adm = Order.objects.all()[:2]

    # Retrieve the first two products
    products = Product.objects.all()[:1]

    # Count the number of registered users
    reg_users = len(User.objects.all())

    # Count the number of products
    all_prods = len(Product.objects.all())

    # Count the number of orders
    all_orders = len(Order.objects.all())

    # Get the registered session value
    registered = request.session.get('registered')

    # Prepare the context data
    context = {
        "title": "Home",
        "orders": orders_user,
        "orders_adm": orders_adm,
        "users": users,
        "products": products,
        "count_users": reg_users,
        "count_products": all_prods,
        "count_orders": all_orders,
        "registered": registered,
    }

    # Render the index template with the context data
    return render(request, "inventory/index.html", context)



def register(request):
    if request.method == "POST":
        # Handle the user registration form submission
        form = UserRegistry(request.POST)
        if form.is_valid():
            form.save()
            request.session['registered'] = True
            return redirect("login")
    else:
        form = UserRegistry()

    # Prepare the context data
    context = {"register": "Register", "form": form}

    # Render the register template with the context data
    return render(request, "inventory/register.html", context)

@login_required
def products(request):
    # Retrieve all products
    products = Product.objects.all()

    if request.method == "POST":
        # Handle the product form submission
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()

    # Prepare the context data
    context = {"title": "Products", "products": products, "form": form}

    # Render the products template with the context data
    return render(request, "inventory/products.html", context)


@login_required
def orders(request):
    # Retrieve all orders
    orders = Order.objects.all()

    # Get the value of the 'my_cookie' cookie
    my_cookie = request.COOKIES.get('my_cookie')

    if request.method == "POST":
        # Handle the order form submission
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect("orders")
    else:
        form = OrderForm()

    # Prepare the context data
    context = {"title": "Orders", "orders": orders, "form": form, "my_cookie": my_cookie}

    # Render the orders template with the context data
    return render(request, "inventory/orders.html", context)


@login_required
def users(request):
    # Retrieve all users
    users = User.objects.all()

    # Prepare the context data
    context = {"title": "Users", "users": users}

    # Render the users template with the context data
    return render(request, "inventory/users.html", context)


@login_required
def user(request):
    # Prepare the context data
    context = {"profile": "User Profile"}

    # Create a response object
    response = render(request, "inventory/user.html", context)

    # Set the 'my_cookie' cookie
    response.set_cookie('my_cookie', 'cookie_value')

    # Return the response
    return response



