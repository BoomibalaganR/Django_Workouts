
from django.contrib import admin
from django.urls import path,include 


urlpatterns = [      
    path('image/', include('imageApp.urls')),
    path('admin/', admin.site.urls),
]
