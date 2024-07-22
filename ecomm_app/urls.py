from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('seller_info/<int:seller_id>/', views.seller_info, name='seller_info'),
    
    path('category/<str:category>', views.category_page, name='category'),

    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),


    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('bought_products/', views.bought_products, name='bought_products'),
    path('my_products/', views.my_products, name='my_products'),   
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('buy_now/', views.buy_now, name='buy_now'),
    path('remove_listed_product/', views.remove_listed_product, name='remove_listed_product'),

]