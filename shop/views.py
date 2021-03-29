from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . models import Category, Product, Cart, CartItem


# Create your views here.
def home(request, category_slug=None, product_slug=None):
    products = Product.objects.all().filter(available=True)
    return render(request, "home.html", {"category": category_slug, "products": products[0:5]})


def category(request, category_slug):
    products = Product.objects.all().filter(available=True)
    pagination = Paginator(list(products), 12)
    return render(request, "categories.html", {
        "pages": [i for i in range(1, pagination.num_pages + 1)],
        "category": category_slug,
        "products_part_1": products[0:5],
        "products_part_2": products[5:10],
        "products_part_3": products[10:12],
    })


def product_description(request, category_slug, product_slug):
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    return render(request, "product_description.html", {'product': product})


def halloween(request):
    return render(request, "halloween.html")


def ceramic(request):
    return render(request, "ceramic.html")


def sweets(request):
    products = Product.objects.all()
    return render(request, "sweets.html", {'products': products[6:11]})


def free_present(request):
    products = Product.objects.all()
    return render(request, "free_present.html", {'products': products[6:11]})


def cart(request):
    return render(request, "cart.html")


def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart.request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect("cart_detail")


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for i in cart_items:
            total += (i.product.price * i.quantity)
            counter += i.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, "cart.html", dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


def cart_delete(request, product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')
