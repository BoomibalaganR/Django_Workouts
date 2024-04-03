from django.urls import path
from . import views 

urlpatterns = [ 
                path('', views.CreateUserView.as_view(), name='user-create'),     
                path('login/',views.UserLoginView.as_view(),name='user-login')
               ]