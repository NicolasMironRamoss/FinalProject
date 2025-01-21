# USER-RELATED VIEWS: 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# MENUITEMS RELATED VIEWS:
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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