from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views  # Import jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


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

    # User authentication routes
    path('auth/register/', views.UserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Other routes
    path('menu-items/', views.MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('cart/menu-items/', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),

]
