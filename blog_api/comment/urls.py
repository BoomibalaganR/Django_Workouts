from django.urls import path 

from . import views


urlpatterns = [ 
              path('', views.CommentListCreateView.as_view() , name='comment-create-list'),  
              path('<str:commentId>',views.CommentRetrieveUpdateDeleteView.as_view(), name='comment-rud'),
            ]