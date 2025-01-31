from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Products, Category
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email', 'password']
        extra_kwargs = {'password':{"write_only":True}}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {'author':{"read_only":True}}
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    