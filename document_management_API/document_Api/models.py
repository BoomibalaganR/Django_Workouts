from django.db import models 
from djongo import models



class Document(models.Model):

    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length = 20)
    size = models.IntegerField(default=0)   
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True) 

    description = models.CharField(max_length=30)
    
    content_type = models.CharField(max_length=10,default=None) 
    storage_path = models.CharField(max_length= 225)  
    url = models.CharField(max_length=225) 
    
    class Meta: 
        db_table = "File" 
    
    def __str__(self) -> str:
        return self.name 


