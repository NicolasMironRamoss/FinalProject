# USER-RELATED VIEWS: 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# MENUITEMS RELATED VIEWS:
# from rest_framework import generics
# from rest_framework.views import APIView
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# CART RELATED VIEWS:
from rest_framework import status # , generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
from .models import Cart, MenuItem
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
# ORDER RELATED VIEWS:
from .models import Order, OrderItem, Cart
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
# USER AUTHENTICATION:
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer, UserCreateSerializer  # Assuming it's in your serializers.py file

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the LittleLemon API!")

# USER-RELATED VIEWS: 

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class LoginView(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        if user.check_password(request.data['password']):
            token = RefreshToken.for_user(user)
            return Response({'access_token': str(token.access_token), 'refresh_token': str(token)})
        return Response({'error': 'Invalid credentials'}, status=400)

# MENUITEMS RELATED VIEWS:

class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# CART RELATED VIEWS:

class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        menuitem_id = self.request.data.get('menuitem')
        quantity = self.request.data.get('quantity')

        # Check if menu item exists
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            raise ValueError("Menu item does not exist")

        # Calculate price and create cart item
        unit_price = menuitem.price
        price = unit_price * quantity

        # Save to the database
        serializer.save(user=user, menuitem=menuitem, quantity=quantity, unit_price=unit_price, price=price)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        quantity = self.request.data.get('quantity')
        menuitem = serializer.instance.menuitem
        unit_price = menuitem.price
        price = unit_price * quantity

        # Update the cart item
        serializer.save(quantity=quantity, price=price)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ORDER RELATED VIEWS:

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        total = 0
        order_items = []

        # Fetch all cart items for the user
        cart_items = Cart.objects.filter(user=user)

        # Calculate total and prepare order items
        for cart_item in cart_items:
            order_items.append(OrderItem(
                order=serializer.instance,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            ))
            total += cart_item.price

        # Create the order
        order = serializer.save(user=user, total=total)

        # Save order items
        for order_item in order_items:
            order_item.save()

        # Clear the cart after placing the order
        cart_items.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


# USER AUTHENTICATION:
class UserViewSet(UserViewSet):
    pass

class CustomLoginView(TokenObtainPairView):
    # Customize the login view if needed
    pass