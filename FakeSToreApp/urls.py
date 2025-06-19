from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',SignupView.as_view(),name='Singup'),
    path('login/',LoginView.as_view(),name='Singup'),
    path("products/",ProductView.as_view(),name = 'Products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product detail by id'),
    path('products/category/',ProductCategoryList.as_view(), name='category list'),
    path('products/category/<str:category>/', ProductsByCategory.as_view(), name='products by category'),
    path('cart/', CartCreateView.as_view(),name='the cart'),               
    path('carts', CartQueryView.as_view(),name='cart by user id'),
     path('products', ProductListView.as_view(),name='view products upto certain limit'),
]

