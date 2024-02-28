from django.views.generic import TemplateView

from django.urls import path 
from . import views 


urlpatterns = [  
    path('', views.get_All_images, name='all-images'),
    path('create/',  TemplateView.as_view(template_name= 'create-page.html'), name='create-image' ), 
    path('upload/', views.upload_image, name = 'upload-image'),    
    path("<image_id>/delete/", views.delete_image, name = 'delete-image'),  
    path('<image_id>/download/', views.download_image, name = 'download-image'),
    
]
