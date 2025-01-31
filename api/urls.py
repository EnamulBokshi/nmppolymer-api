from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user_list'),
    path('create-category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('products/',views.ProductList.as_view(), name='product_list'),
    path('products-create/', views.ProductCreate.as_view(), name='product_list_create'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product/delete/<int:pk>/', views.ProductDelete.as_view(), name='product_delete'),
    ]   