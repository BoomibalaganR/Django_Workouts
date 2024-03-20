
from django.urls import path,include 
from . import views

externalpatterns = [
    path('',views.DocumentListView.as_view(),name='all-document'),  
    path('add/',views.DocumentCreateView.as_view(),name='add-document'),
    path("<str:name>/update/",views.DocumentUpdateView.as_view(), name = 'update-document'),
    path("<str:name>/delete/",views.DocumentDeleteView.as_view(), name = 'delete-document'),  
    path('<str:name>/download/',views.DocumentDownloadView.as_view(), name = 'download-document'), 
    path('<str:name>/',views.DocumentDetailView.as_view(), name="single-document"), 
] 


urlpatterns = [ 
    path('documents/', include(externalpatterns), name='document'), 
    path('login/',views.LoginAPIView.as_view(), name='user-login'),
   
]
