from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import generics,status,viewsets
from .models import Products,Category
from .serializers import ProductSerializer,CategorySerializer,UserSerializer

# User APIs

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

'''
    products apis sett
'''

class ProductList(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetail(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductCreate(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdate(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDelete(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListByUser(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Products.objects.filter(author=self.request.user)

'''
category apis
'''

class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryUpdate(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDelete(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
