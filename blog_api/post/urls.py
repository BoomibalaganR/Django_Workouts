from django.urls import path
from . import views 

urlpatterns = [ 
                path('', views.PostListCreateView.as_view(), name='post-read-create'),    
                path('<str:postId>', views.PostRetrieveUpdateDestroy.as_view(), name='post-rud'), 
                
               ]