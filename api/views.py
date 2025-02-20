from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Contact, News, Products, Category, Slider, Testimonial
from .serializers import ContactSerializer, NewsSerializer, ProductSerializer, CategorySerializer, TestimonialSerializer, UserSerializer, SliderSerializer
import os

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

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Product APIs
class ProductList(generics.ListAPIView):
    queryset = Products.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Products.objects.filter(category=category_id)

class ProductListBySearch(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        search_query = self.request.GET.get('search','').strip()
        if search_query:
            return Products.objects.filter(name__icontains=search_query)
        return Products.objects.all()

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
        product = self.get_object()
        if product.author != self.request.user:
            return Response({'error': 'You do not have permission to update this product'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDelete(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        
        # Check permission
        if product.author != request.user:
            return Response(
                {'error': 'You do not have permission to delete this product'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Delete associated media files
        media_fields = ['image', 'image2', 'image3', 'image4']
        for field in media_fields:
            media_file = getattr(product, field)
            if media_file:
                try:
                    # Delete the file from storage
                    if os.path.isfile(media_file.path):
                        os.remove(media_file.path)
                    # Try to remove empty directory if exists
                    directory = os.path.dirname(media_file.path)
                    if os.path.exists(directory) and not os.listdir(directory):
                        os.rmdir(directory)
                except Exception as e:
                    print(f"Error deleting media file {field}: {str(e)}")
        
        # Delete the product
        self.perform_destroy(product)
        return Response(
            {'message': 'Product and associated media files deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )

class ProductListByUser(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Products.objects.filter(author=self.request.user)


#  Category APIs
class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category_name = serializer.validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            raise Response({'error': 'Category already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

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
        category = self.get_object()
        self.perform_destroy(category)
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


#  Slider APIs
class SliderCreate(generics.CreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SliderList(generics.ListAPIView):
    queryset = Slider.objects.all().order_by('-created_at')
    serializer_class = SliderSerializer
    permission_classes = [AllowAny]

class SliderDetail(generics.RetrieveAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [AllowAny]

class SliderUpdate(generics.UpdateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        slider = self.get_object()
        if slider.author != self.request.user:
            return Response({'error': 'You do not have permission to update this slider'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SliderDelete(generics.DestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        slider = self.get_object()
        if slider.author != request.user:
            return Response({'error': 'You do not have permission to delete this slider'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(slider)
        return Response({'message': 'Slider deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


#  Contact APIs
class ContactCreate(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ContactList(generics.ListAPIView):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

class ContactDetail(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

class ContactUpdate(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ContactDelete(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        contact = self.get_object()
        self.perform_destroy(contact)
        return Response({'message': 'Contact deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class ContactMarkRead(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        contact = self.get_object()
        serializer.save(is_read=True)
        return Response({'message': 'Contact marked as read'}, status=status.HTTP_200_OK)

class ContactMarkResponded(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        contact = self.get_object()
        serializer.save(is_responded=True)
        return Response({'message': 'Contact marked as responded'}, status=status.HTTP_200_OK)

class ContactMarkUnread(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        contact = self.get_object()
        serializer.save(is_read=False)
        return Response({'message': 'Contact marked as unread'}, status=status.HTTP_200_OK)

class ContactMarkUnresponded(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        contact = self.get_object()
        serializer.save(is_responded=False)
        return Response({'message': 'Contact marked as unresponded'}, status=status.HTTP_200_OK)

class ContactListByCategory(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Contact.objects.filter(category=category)


# News APIs
class NewsList(generics.ListAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

class NewsDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

class NewsCreate(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsUpdate(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        news = self.get_object()
        if news.author != self.request.user:
            return Response({'error': 'You do not have permission to update this news'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDelete(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        news = self.get_object()
        if news.author != request.user:
            return Response({'error': 'You do not have permission to delete this news'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(news)
        return Response({'message': 'News deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class NewsListByUser(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return News.objects.filter(author=self.request.user)


# Testimonial APIs
class TestimonialList(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]

class TestimonialDetail(generics.RetrieveAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]

class TestimonialCreate(generics.CreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestimonialUpdate(generics.UpdateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        testimonial = self.get_object()
        if testimonial.author != self.request.user:
            return Response({'error': 'You do not have permission to update this testimonial'}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestimonialDelete(generics.DestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        testimonial = self.get_object()
        if testimonial.author != request.user:
            return Response({'error': 'You do not have permission to delete this testimonial'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(testimonial)
        return Response({'message': 'Testimonial deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    