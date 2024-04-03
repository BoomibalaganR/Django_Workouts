from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404 )
from rest_framework import status 
from rest_framework.response import Response  
from rest_framework.exceptions import ValidationError 

from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from bson import ObjectId  
from bson.errors import InvalidId

from .models import Comment,Post 
from .serializers import CreateCommentSerializer, UpdateCommentSerializer 

from blog_api.permissions import IsOwnerOrReadOnly



class CommentListCreateView(ListCreateAPIView):
   
    serializer_class = CreateCommentSerializer    
    
      
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
    
    def perform_create(self, serializer): 
        serializer.context['user'] = self.request.user
        return super().perform_create(serializer)
    
    
    def list(self, request, *args, **kwargs): 
        
        # Retrieve the query parameter value from the request
        post_id_str = self.request.query_params.get('postId') 
        
        # check query parameter exit or not  
        if post_id_str is None: 
           return Response(data={'error':'The "post_id" parameter is required'},
                           status=status.HTTP_400_BAD_REQUEST) 
         
        # convert string into ObjectID   
        # check if post exit or not  
        try:  
            pk = ObjectId(post_id_str) 
            get_object_or_404(Post.objects.all(), pk=pk)   
            return super().list(request, *args, **kwargs) 
        
        except Post.DoesNotExist: 
            return Response(data={'error': 'post does not exit'},
                            status=status.HTTP_404_NOT_FOUND)
        except (TypeError, ValueError, InvalidId):
            return Response(data={'error': "Invalid format for post_id"},
                            status=status.HTTP_400_BAD_REQUEST) 
        
    def get_queryset(self):
        # Retrieve the query parameter value from the request
        post_id = ObjectId(self.request.query_params.get('postId') )
        print("=====>>>>",post_id)
        # Filter the queryset by the foreign key field
        queryset = Comment.objects.filter(post=post_id) 
        return queryset



class CommentRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):   
    
    queryset = Comment.objects.all()
    serializer_class = UpdateCommentSerializer 
    
    http_method_names = [
        "get",
        "patch",
        "delete",
    ] 
    
    def get_authenticators(self):
        if self.request.method in ("PATCH","DELETE"):
            # For POST requests, use TokenAuthentication
            return [JWTStatelessUserAuthentication()] 
        
    
    def get_permissions(self):
        if self.request.method in ("PATCH", "DELETE"):
            # For POST requests (creating posts), only authenticated users are allowed
            return [IsAuthenticated(),IsOwnerOrReadOnly()]
        else:
            # For GET requests (reading posts), allow any user (including unauthenticated users)
            return [AllowAny()]
    
    
   
    def get_object(self): 
        try:
            pk = ObjectId(self.kwargs.get('commentId'))
            obj =   get_object_or_404(self.get_queryset(), pk=pk)  
        except (TypeError, ValueError, InvalidId):
            raise ValidationError("Invalid format for comment_id") 
        self.check_object_permissions(self.request, obj)
        return obj
       
    def partial_update(self, request, *args, **kwargs):
    
        response = super().partial_update(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully comment updated!!'} 
        return response   
             
    def destroy(self, request, *args, **kwargs):
        response =  super().destroy(request, *args, **kwargs) 
        response.data = {'error': False, 'message': 'successfully comment deleted!!'} 
        return response 
    






    
    