from django.db import models 

class ImageMetadata(models.Model):

    name = models.CharField(max_length = 20)
    size = models.IntegerField(default=0) 
    content_type = models.CharField(max_length=5,default="none") 
    storage_path = models.CharField(max_length= 225)  
    url = models.CharField(max_length=225)

    class Meta: 
        db_table = "ImageMetadata" 
    
    def __str__(self) -> str:
        return self.name