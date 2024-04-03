from django.contrib import admin
from django.urls import path,include  

externalpatterns = [         
    path("posts/", include('post.urls'), name='blog-post'),   
    path('comments/', include('comment.urls'), name='comment-url'), 
    path('users/', include('author.urls'), name='user-url'),
] 
 
urlpatterns = [
    path("api/v1/",include(externalpatterns))
]


    