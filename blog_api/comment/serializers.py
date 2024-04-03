from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, Post, User    
from post.serializers import PostSerializer,AuthorSerializer  


from bson.errors import InvalidId
from bson import ObjectId   



class CreateCommentSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(write_only=True)  
   # post = PostSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['_id', 'content', 'author','post_id','created_at']
        read_only_field=('created_at',)
   
   
    def create(self, validated_data):
        
        # pop the post_id from validated_data
        post_id_str = validated_data.pop('post_id')
        print("validated-data",validated_data)
        # get post using post_id 
        # handle error if post does not exit,
        # invalid post id
        try: 
            post_obj = Post.objects.get(_id=ObjectId(post_id_str)) 
            print("====>>>>",post_obj)
        except Post.DoesNotExist:
            raise ValidationError("Specified post_id does not exist") 
        except (TypeError, ValueError, InvalidId):
            raise ValidationError("Invalid format for post_id")
    
        # create new comment 
        # return comment instance 
        user = self.context.get('user') 
        comment_obj = Comment.objects.create(post=post_obj, 
                                             author=User.objects.get(_id=ObjectId(user.id)), 
                                             **validated_data) 
        return comment_obj 
    
    
    
class UpdateCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['_id', 'content'] 

   