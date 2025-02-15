from django.urls import path
from . import views

urlpatterns = [
    # User Management
    path('users/', views.UserList.as_view(), name='user_list'),
    # path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    # path('users/update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    
    # Categories
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/create/', views.CreateCategoryView.as_view(), name='create_category'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('categories/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category_delete'),
    
    # Products
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/create/', views.ProductCreate.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('products/update/<int:pk>/', views.ProductUpdate.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', views.ProductDelete.as_view(), name='product_delete'),
    path('products/my/', views.ProductListByUser.as_view(), name='my_products'),  # Get user-specific products
    path('products/category/<int:pk>/', views.ProductListByCategory.as_view(), name='products_by_category'),
    path('products/search/', views.ProductListBySearch.as_view(), name='products_by_search'),

    # Sliders
    path('sliders/', views.SliderList.as_view(), name='slider_list'),
    path('sliders/create/', views.SliderCreate.as_view(), name='slider_create'),
    path('sliders/<int:pk>/', views.SliderDetail.as_view(), name='slider_detail'),
    path('sliders/update/<int:pk>/', views.SliderUpdate.as_view(), name='slider_update'),   
    path('sliders/delete/<int:pk>/', views.SliderDelete.as_view(), name='slider_delete'),
    
    # Contacts
    path('contacts/', views.ContactList.as_view(), name='contact_list'),
    path('contacts/create/', views.ContactCreate.as_view(), name='contact_create'),
    path('contacts/<int:pk>/', views.ContactDetail.as_view(), name='contact_detail'),
    path('contacts/update/<int:pk>/', views.ContactUpdate.as_view(), name='contact_update'),
    path('contacts/delete/<int:pk>/', views.ContactDelete.as_view(), name='contact_delete'),
    

    # News
    path('news/', views.NewsList.as_view(), name='news_list'),
    path('news/create/', views.NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/', views.NewsDetail.as_view(), name='news_detail'),
    path('news/update/<int:pk>/', views.NewsUpdate.as_view(), name='news_update'),
    path('news/delete/<int:pk>/', views.NewsDelete.as_view(), name='news_delete'),
    
    # Testimonials
    path('testimonials/', views.TestimonialList.as_view(), name='testimonial_list'),
    path('testimonials/create/', views.TestimonialCreate.as_view(), name='testimonial_create'),
    path('testimonials/<int:pk>/', views.TestimonialDetail.as_view(), name='testimonial_detail'),
    path('testimonials/update/<int:pk>/', views.TestimonialUpdate.as_view(), name='testimonial_update'),
    path('testimonials/delete/<int:pk>/', views.TestimonialDelete.as_view(), name='testimonial_delete'),
    

]
