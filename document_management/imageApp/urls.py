from django.views.generic import TemplateView

from django.urls import path 
from . import views  
from .View import Image_crud


urlpatterns = [  
   
    path('',Image_crud.ImageListView.as_view(),name='all-images'), 
    
    path('create/', Image_crud.ImageCreateView.as_view(), name='create-image'),    
    path("<int:pk>/delete/", Image_crud.ImageDeleteView.as_view(), name = 'delete-image'),  
    path('<int:pk>/download/',Image_crud.ImageDownloadView.as_view(), name = 'download-image'), 
    path('<str:name>/',Image_crud.ImageDetailView.as_view(), name="single-image"),
    
]
