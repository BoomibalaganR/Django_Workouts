from django.db import models 
from djongo import models 
from djongo.models.fields import ObjectIdField

from author.models import User

class Post(models.Model): 
    
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=20,blank=False) 
    content = models.TextField(blank=False) 
    
    author = models.ForeignKey(to=User, 
                               on_delete=models.CASCADE, 
                               related_name='post',
                               blank=False)
    
    publication_date = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    
    class Meta: 
        ordering = ['updated_at'] 
        db_table = 'post' 
    
    def __str__(self) -> str:
        return self.title
