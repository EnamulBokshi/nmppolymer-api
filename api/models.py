import os
from uuid import uuid4
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
import cloudinary
import cloudinary.uploader
import cloudinary.api


def upload_path(instance, filename):
    """
    Generate a clean, unique path for product images.
    Format: products/category_name/product_id_uuid.extension
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    
    # Generate a unique filename using UUID
    unique_filename = f"{instance.id}_{uuid4().hex[:8]}.{ext}"
    
    # Get category name and clean it
    category_name = slugify(instance.category.name) if instance.category else 'uncategorized'
    
    # Build the path
    return os.path.join('products', category_name, unique_filename)

def slider_file_path(instance, filename):
    """
    Generate a clean, unique path for slider files.
    Format: slider/uuid_filename.extension
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid4().hex[:8]}_{slugify(instance.name)}.{ext}"
    return os.path.join('slider', unique_filename)
def news_file_path(instance, filename):
    """
    Generate a clean, unique path for news images.
    Format: news/news_id_uuid.extension
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{instance.id}_{uuid4().hex[:8]}.{ext}"
    return os.path.join('news', unique_filename)

def testimonial_file_path(instance, filename):
    """
    Generate a clean, unique path for testimonial images.
    Format: testimonial/testimonial_id_uuid.extension
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{instance.id}_{uuid4().hex[:8]}.{ext}"
    return os.path.join('testimonial', unique_filename) 


class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to=upload_path, null=True, blank=True)
    image2 = models.ImageField(upload_to=upload_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=upload_path, null=True, blank=True)
    image4 = models.ImageField(upload_to=upload_path, null=True, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Slider(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False,default='Slider')
    video = models.FileField(upload_to=slider_file_path,null=False, blank=False)
    caption = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.caption
    
class Contact(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return self.firstName
    
class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to=news_file_path, null=True, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to=testimonial_file_path, null=True, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

