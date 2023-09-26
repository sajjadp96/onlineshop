from django.urls import path
from product.views import CategoryList,ProductList

urlpatterns = [
    path('categories/', CategoryList.as_view(),name='categories'),
    path('products/', ProductList.as_view(),name='products'),    
]