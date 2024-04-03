from rest_framework.fields import empty
from rest_framework import serializers  

from .models import Post  
from bson import ObjectId 

from author.models import User 
from author.serializers import AuthorSerializer

      
class PostSerializer(serializers.ModelSerializer):   
    #author = serializers.SerializerMethodField()  # Use SerializerMethodField for custom representation
    author = AuthorSerializer(read_only=True)
    
    class Meta: 
        model = Post 
        fields = ['_id','title','content', 'author'] 
        extra_kwargs = {
            'author': {'required': False},  
        }
    
    def create(self, validated_data):  
        validated_data['author'] = User.objects.get(username='rolex') #autheticated author
        return super().create(validated_data) 
    
    
    # def get_author(self, post_instance): 
        # get author object from post_instance
        author = post_instance.author 
        # get author _id from author object
        author_id = author._id 
        # get author instance from db
        author_instance = User.objects.get(pk=author_id) 
        
        # Serialize the Author instance using the AuthorSerializer
        author_serializer = AuthorSerializer(author_instance) 
        return author_serializer.data



