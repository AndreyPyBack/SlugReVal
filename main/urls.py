from django.urls import path
from .views import register, product_detail, ProductDetailView, add_product, product_list, ProductListView, login_view, \
    logout

urlpatterns = [
    path('products/', product_list, name='product-list-func'),
    path('products/class/', ProductListView.as_view(), name='product-list-class'),
    path('register/', register, name='register'),
    path('product/<slug:slug>/', product_detail, name='product-detail-func'),
    path('product/<slug:slug>/class/', ProductDetailView.as_view(), name='product-detail-class'),
    path('add-product/', add_product, name='add-product'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout')
]
