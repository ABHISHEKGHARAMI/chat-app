from django.urls import path
from chat.views.home_view import userprofile, home_view
from chat.views.user_view import signup,editProfile,loginPage

urlpatterns = [
    path("",loginPage,name='login'),
    path("signup/",signup,name='signup'),
    path('user/',home_view,name='home'),
    path('edit/',editProfile,name='edit'),
    path('user/<str:username>/',userprofile,name='username'),
]
