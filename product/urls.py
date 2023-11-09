from django.urls import path
from product.views import CategoryList,ProductList,SearchView,HelloView,CategoryDetailView,ProductDetailView,AddProductView,AddCategory,UpdateCategroryView,UpdateProductView

urlpatterns = [
    path('categories/', CategoryList.as_view(),name='categories'),
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category_details"),
    path('product/<int:pk>/',ProductDetailView.as_view(),name='product_detail'),
    path('products/', ProductList.as_view(),name='products'),
    path('search/',SearchView.as_view(),name='search'),
    path('',HelloView.as_view(), name ='hello'),
    path('product/add/', AddProductView.as_view()),
    path('product/delete/', AddProductView.as_view()),
    path('category/delete/', AddCategory.as_view()),
    path('category/add/', AddCategory.as_view()),
    # path('products/', ProductList.as_view()),   
]