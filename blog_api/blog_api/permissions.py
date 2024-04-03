from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True 
        print("===>>",type(obj.author._id), "__===>>",type(request.user))
        # Write permissions only allowed who create the post 
        
        return str(obj.author._id) == request.user.id