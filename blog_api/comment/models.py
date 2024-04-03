from django.db import models 
from djongo import models
from author.models import User

from post.models import Post


class Comment(models.Model): 
    
    _id = models.ObjectIdField(primary_key=True) 
    content = models.TextField(blank=False) 
    #parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, 
    # null=True, blank=True, related_name='replies')

    post = models.ForeignKey(to= Post, 
                             on_delete=models.CASCADE, 
                             related_name='comments',
                             blank=False) 
    
    author = models.ForeignKey(to=User, 
                             on_delete=models.CASCADE,
                             related_name='comments',
                             blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    
    class Meta: 
        ordering = ['updated_at'] 
        db_table = 'comment'  
        
 
    