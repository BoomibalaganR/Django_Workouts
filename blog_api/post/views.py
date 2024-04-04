from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, 
                                     get_object_or_404)     
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication,JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import (ValidationError)
from rest_framework.pagination import PageNumberPagination 

from bson import ObjectId  
from bson.errors import InvalidId 

from .serializers import PostSerializer
from .models import Post   

from blog_api.permissions import IsOwnerOrReadOnly


class PostListCreateView(ListCreateAPIView):  
   
    queryset = Post.objects.all() 
    serializer_class = PostSerializer     
    
     
    def get_authenticators(self):
        if self.request.method == 'POST':
            # For POST requests, use TokenAuthentication
            return [JWTStatelessUserAuthentication()] 
        
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # For POST requests (creating posts), only authenticated users are allowed
            return [IsAuthenticated()]
        else:
            # For GET requests (reading posts), allow any user (including unauthenticated users)
            return [AllowAny()]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully posted!!'} 
        return response
    
    def list(self, request, *args, **kwargs):
        response =  super().list(request, *args, **kwargs) 
        print(response) 
        return response
    
   
class PostRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView): 
    queryset = Post.objects.all() 
    serializer_class = PostSerializer   
    
    http_method_names = [
        "get",
        "patch",
        "delete",
        
    ]
       
    def get_authenticators(self):
        if self.request.method in ('PATCH',"DELETE"):
            # For POST requests, use TokenAuthentication
            return [JWTStatelessUserAuthentication()] 
        
    
    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            # For POST requests (creating posts), only authenticated users are allowed
            return [IsAuthenticated(),IsOwnerOrReadOnly()]
        else:
            # For GET requests (reading posts), allow any user (including unauthenticated users)
            return [AllowAny()]
    
     
     
    def get_object(self): 
        try:
            pk = ObjectId(self.kwargs.get('postId'))
            obj =  get_object_or_404(self.get_queryset(), pk=pk)   
           
        except (TypeError, ValueError, InvalidId):
            raise ValidationError("Invalid format for post_id") 
        self.check_object_permissions(self.request, obj)
        return obj  
    
     
    def retrieve(self, request, *args, **kwargs):
        response =  super().retrieve(request, *args, **kwargs) 
        print(response) 
        return response
        
    def partial_update(self, request, *args, **kwargs):
    
        response = super().partial_update(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully updated!!'} 
        return response   
             
    def destroy(self, request, *args, **kwargs):
        response =  super().destroy(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully deleted!!'} 
        return response 
    
