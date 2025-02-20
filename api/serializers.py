import os
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import News, Products, Category, Slider, Contact, Testimonial

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'author', 'author_name', 'image', 'image2', 'image3', 'image4', 'created_at']
        extra_kwargs = {'author': {"read_only": True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'
        extra_kwargs = {
            'author': {"read_only": True},
            'video': {"write_only": True}
        }

    def get_video_url(self, obj):
        if obj.video:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video.url)
        return None

    def validate_video(self, value):
        max_size = 100 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('Video size is too large')

        valid_extensions = ['.mp4', '.webm', '.mov']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError('Unsupported file extension')
        return value

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'author', 'author_name', 'image', 'created_at']
        extra_kwargs = {'author': {"read_only": True}}

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        extra_kwargs = {'author': {"read_only": True}}