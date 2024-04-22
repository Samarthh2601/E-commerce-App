from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('bought_products/', views.bought_products, name='bought_products'),
    path('buy_now/', views.buy_now, name='buy_now'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('my_products/', views.my_products, name='my_products'),   
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category>', views.category_page, name='category')

]