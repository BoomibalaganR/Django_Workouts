from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate 

from .utils import get_tokens_for_user
from .serializers import AuthorSerializer
from django.db import IntegrityError

class CreateUserView(CreateAPIView):   
     
     permission_classes = [AllowAny]  # Allow unauthenticated access
     serializer_class = AuthorSerializer  
     
     def create(self, serializer): 
          try:
               response =  super().create(serializer) 
               return Response({'message': 'User created successfully', 'user': response.data}, 
                               status=status.HTTP_201_CREATED)
          except Exception as e:
            # Handle the case where the username already exists
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


   
 
class UserLoginView(APIView):  
     permission_classes = [AllowAny]  # Allow unauthenticated access

     def post(self, request):
          # Retrieve username and password from request data
          username = request.data.get('username')
          password = request.data.get('password')
          print("======>>>>",request.data)
          #user_instance = User.objects.get(username=username) 
          
          try: 
               user = authenticate(username=username, password=password)  
               if user is not None: 
                    import jwt 
                    from blog_api.settings import SECRET_KEY
                    
                    # Generate JWT token for the authenticated user
                    token = get_tokens_for_user(user=user)  
                   
                    decoded_token = jwt.decode(token.get('access'),SECRET_KEY, algorithms=["HS256"])  
                    print('payload',decoded_token)
                    serializer = AuthorSerializer(user)
                    
                    # Return token as response
                    return Response({'token': token['access'],'user':serializer.data}, 
                                    status=status.HTTP_200_OK)   
          except Exception as e: 
                    return Response({'error': str(e)}, 
                               status=status.HTTP_400_BAD_REQUEST)
           
          return Response({'error': "invalid credential"}, 
                               status=status.HTTP_401_UNAUTHORIZED)
           

         