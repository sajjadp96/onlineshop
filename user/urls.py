from django.urls import path
from user.views import RigisterView,LoginView, AuthenticateRefreshToken,VerifyView,LogoutView,AddressView,ProfileView,UserInfoView,AdminRegisterView
from order.views import AllOrdersView

urlpatterns = [
    path('rigister/', RigisterView.as_view(),name='rigister'),
    path('login/',LoginView.as_view(),name='login'),
    path('refresh_token/',AuthenticateRefreshToken.as_view()),
    path('verify/',VerifyView.as_view()),  
    path('logout/',LogoutView.as_view()),
    path('address/',AddressView.as_view()),
    path('profile/',ProfileView.as_view()), 
    path('user_info/',UserInfoView.as_view()), 
    path('admin/',AdminRegisterView.as_view()),
    path('admin/login/',LoginView.as_view()),
    path('admin/sendorder/',AllOrdersView.as_view(),)
]