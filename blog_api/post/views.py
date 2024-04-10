from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, 
                                     get_object_or_404) 
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import (ValidationError)  
from rest_framework.throttling import (AnonRateThrottle,UserRateThrottle)

from django.core.cache import cache as django_cache  

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from bson import ObjectId  
from bson.errors import InvalidId 

from .serializers import PostSerializer
from .models import Post   

from blog_api.permissions import IsOwnerOrReadOnly



GET_ALL_RECORDS_CACHE_KEY = 'all_records_'
GET_SINGLE_RECORD_CACHE_ = 'single_record_' 
TIMEOUT = 60*2

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
    
    
    def get_throttles(self): 
        
        if self.request.method == "GET" and 'Authorization' in self.request.headers:  
            return [UserRateThrottle()]  
        elif self.request.method == "GET" and 'Authorization' not in self.request.headers:  
            return [AnonRateThrottle()]
        
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully posted!!'} 
        return response 
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)  
    
         
    @method_decorator(cache_page(timeout=TIMEOUT, key_prefix=GET_SINGLE_RECORD_CACHE_)) 
    def list(self, request, *args, **kwargs):
       
        print("\n------->>>>>>>>>","no cache available..")  

        response = super().list(request, *args, **kwargs)
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
    
    def get_throttles(self): 
        
        # if self.request.method == "GET" and 'Authorization' in self.request.headers :  
        if self.request.method == "GET" and 'Authorization' not in self.request.headers:  
            return [AnonRateThrottle()]
        
        return [UserRateThrottle()]  
        
    def get_object(self): 
        try:
            pk = ObjectId(self.kwargs.get('postId'))
            obj =  get_object_or_404(self.get_queryset(), pk=pk)   
           
        except (TypeError, ValueError, InvalidId):
            raise ValidationError("Invalid format for post_id") 
        
        self.check_object_permissions(self.request, obj)
        return obj  
    
    @method_decorator(cache_page(timeout=TIMEOUT, key_prefix=GET_SINGLE_RECORD_CACHE_))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 
    
    def retrieve(self, request, *args, **kwargs):
        response =  super().retrieve(request, *args, **kwargs)   
        print("--->>>>no cache available")
        print(response) 
        return response
            
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully updated!!'}  
        
        try:
            # delete cache
            django_cache.delete_pattern(f'*{GET_ALL_RECORDS_CACHE_KEY}*')   
            django_cache.delete_pattern(f'*{GET_SINGLE_RECORD_CACHE_}*')  
            print('delete cached data because resourse was changed\n')  
        except Exception as e:
            print("Exception while caching response:", e)  
            
        return response 
     
    def destroy(self, request, *args, **kwargs):
        response =  super().destroy(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully deleted!!'}  
        
        try:
            # delete cache
            django_cache.delete_pattern(f'*{GET_ALL_RECORDS_CACHE_KEY}*')   
            django_cache.delete_pattern(f'*{GET_SINGLE_RECORD_CACHE_}*')  
            print('delete cached data because resourse was changed')
        except Exception as e:
            print("Exception while caching response:", e) 
              
        return response 
    
