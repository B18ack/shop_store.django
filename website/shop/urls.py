from django.urls import path, include
from . import views

urlpatterns = [
    path('cart/', include('cart.urls', namespace='cart')),
    
    path('', views.home_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('shop/', views.shop_view, name='shop'),
    path('contact/', views.contact_view, name='contact'),
    path('shop-cart/', views.shop_cart_view, name='shop-cart'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('not_available/', views.not_available_view, name='not_available'),

    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
