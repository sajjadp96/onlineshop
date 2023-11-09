from django.urls import path
from .views import AddOrderView,OrdersView,OrderDetailsView

urlpatterns = [
    path('add/',AddOrderView.as_view(),name='add_order'),
    path('delete/<int:pk>/',AddOrderView.as_view()),
    path('All/',OrdersView.as_view(),name='orders'),
    path('details/<int:pk>/',OrderDetailsView.as_view()),
    path('update/<int:pk>/',OrderDetailsView.as_view()),
    path('deleteitems/',OrderDetailsView.as_view()),   
]