
from django.contrib import admin
from django.urls import path,include

urlpatterns = [ 
    path('api/v1/', include('document_Api.urls'), name='document-api'),
    path('admin/', admin.site.urls),
]
