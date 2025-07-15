from . import models
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegistrationForm, ContactForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, CommentForm, ProductForm
from django.contrib.auth import login, logout
from django.contrib import messages
from slugify import slugify
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail



def home_view(request):
    static_product = ["1", "2", "3", "4", "5", "6", "7", "8"]
    products = models.Product.objects.all()
    static_instas = ["1", "2", "3", "4", "5", "6"]
    media_instas = models.InstagramImage.objects.all()
    return render(request, 'shop/home.html', {
        'static_product': static_product,
        'products': products,
        'static_instas': static_instas,
        'media_instas': media_instas,
    })

def search_view(request):
    query = request.GET.get('q')
    products = models.Product.objects.filter(title__iregex=query)
    products = products.exclude(slug__isnull=True).exclude(slug='')

    context = {
        'products': products,
        'total_product': products.count(),
        'query': query
    }
    return render(request, 'shop/search.html', context)


def contact_view(request):
    static_instas = ["1", "2", "3", "4", "5", "6"]
    media_instas = models.InstagramImage.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                subject=f"Message from the website from {cd['name']}",
                message=(
                    f"Name: {cd['name']}\n"
                    f"Email: {cd['email']}\n"
                    f"Website: {cd['website']}\n"
                    f"Message:\n{cd['message']}"
                ),
                from_email=cd['email'],
                recipient_list=['javaj2006@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'shop/contact.html', {
        'static_instas': static_instas,
        'media_instas': media_instas,
        'form': form,
    })


def product_detail_view(request, slug):
    product = models.Product.objects.get(slug=slug)
    comments = models.Comment.objects.filter(product=product)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            messages.success(request, 'Отзыв успешно добавлен')
            return redirect('product_detail', slug=product.slug)
    else:
        form = CommentForm()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = models.Favorite.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'comments': comments,
        'form': form,
        'total_comments': comments.count(),
        'is_favorite': is_favorite 
    }

    return render(request, 'shop/product_detail.html', context)

def shop_view(request):
    query_params = request.GET.get('category')
    page = request.GET.get('page')

    products = models.Product.objects.all()

    favorites_ids = []
    if request.user.is_authenticated:
        favorites_ids = models.Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)


    if query_params:
        products = products.filter(category__slug=query_params)

    paginator = Paginator(products, 9)  
    
    products = paginator.get_page(page)
    
    categories = models.Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'slug': query_params
    }
    return render(request, 'shop/shop.html', context)

def profile_view(request):
    return render(request, 'shop/profile.html')

def not_available_view(request):
    return render(request, 'shop/not_available.html')

def shop_cart_view(request):
    return render(request, 'shop/shop-cart.html')

def profile_view(request):
    return render(request, 'shop/profile.html')


@login_required(login_url='login')
def add_to_favorites(request, product_id):
    product = get_object_or_404(models.Product, id=product_id)
    models.Favorite.objects.get_or_create(user=request.user, product=product)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')


@login_required(login_url='login')
def remove_from_favorites(request, product_id):
    product = get_object_or_404(models.Product, id=product_id)
    models.Favorite.objects.filter(user=request.user, product=product).delete()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('favorite_list')


@login_required(login_url='login')
def favorite_list(request):
    favorites = models.Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/favorites.html', {'favorites': favorites})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
        else:
            for i in form:
                for e in i.errors:
                    print(e)
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'shop/registration.html', context)
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged into your account')
                return redirect('home')
            else:
                messages.error(request, 'User not found')
        else:

            messages.error(request, 'Incorrect login or password') 
    else:
        form = LoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'shop/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')
