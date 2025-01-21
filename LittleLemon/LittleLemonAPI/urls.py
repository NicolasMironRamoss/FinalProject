from django.urls import path
from . import views

urlpatterns = [
    # User-related endpoints
    path('users/', views.UserCreateView.as_view(), name='user-create'),
    path('users/me/', views.UserDetailView.as_view(), name='user-detail'),
    path('token/login/', views.LoginView.as_view(), name='login'),
    
    # MenuItem-related endpoints
    path('menu-items/', views.MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-item-detail'),
    
    # Cart-related endpoints
    path('cart/menu-items/', views.CartListCreateView.as_view(), name='cart-list-create'),
    
    # Order-related endpoints
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
]
