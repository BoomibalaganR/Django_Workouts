from rest_framework import serializers  
from .models import User  
from django.contrib.auth.hashers import make_password


class AuthorSerializer(serializers.ModelSerializer): 
    pk = serializers.CharField(source='_id', read_only=True) 
    password = serializers.CharField( write_only=True)  # Define write-only field

    class Meta:
        model = User
        fields = [ 'username', 'pk', 'password']      
        
        
    
    def create(self, validated_data): 
        print("validated-data",validated_data)
        #validated_data['password'] = make_password(validated_data.pop('password'))
        return User.objects.create_user(**validated_data) 



# from rest_framework_simplejwt.serializers import TokenObtainSerializer

# class CustomTokenObtainSerializer(TokenObtainSerializer):
#     """
#     Custom token serializer inheriting from TokenObtainSerializer.
#     """
#     @classmethod
#     def get_token(cls, user):
#         # Get the default token
#         token = super().get_token(user)

#         # Add extra information to the token
#         token['username'] = user.username
       
#         return token

       