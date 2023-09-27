from django.urls import path
from product.views import CategoryList,ProductList,SearchView

urlpatterns = [
    path('categories/', CategoryList.as_view(),name='categories'),
    path('products/', ProductList.as_view(),name='products'),
    path('search/',SearchView.as_view(),name='search')    
]