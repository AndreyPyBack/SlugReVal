from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Product
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.views.generic import ListView
from .models import VisitedPage


@login_required
def product_list(request):
    products = Product.objects.all()
    response = render(request, 'product_list.html', {'products': products})
    response = set_cookie(request, response)
    return response


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def set_cookie(request, response):
    if request.COOKIES.get('visit_count'):
        visit_count = int(request.COOKIES.get('visit_count')) + 1
    else:
        visit_count = 1
    response.set_cookie('visit_count', str(visit_count))
    return response


def logout(request):
    if request.user.is_authenticated:
        visited_pages = []
        # Получаем все посещенные страницы для текущего пользователя из куки
        visited_cookies = request.COOKIES.get('visit_count')
        print(visited_cookies)
        if visited_cookies:
            visited_pages = visited_cookies.split(',')
        # Сохраняем посещенную страницу в базу данных
        for page in visited_pages:
            VisitedPage.objects.create(user=request.user, page_name=page)
        # Удаляем куки
        logout(request)
        response = redirect('login')
        response.delete_cookie('visit_count')
        return response
    else:
        # Если пользователь не аутентифицирован, просто перенаправляем его на страницу входа
        return redirect('login')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product-list-func')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
