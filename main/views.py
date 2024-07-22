from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Product
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.views.generic import ListView


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


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
