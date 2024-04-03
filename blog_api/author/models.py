from django.contrib.auth.models import AbstractUser ,UserManager

from djongo.models.fields import ObjectIdField 
from bson.objectid import ObjectId

class User(AbstractUser):
    _id = ObjectIdField(primary_key=True, default=ObjectId, editable=False)  
   # objects = UserManager()

    class Meta: 
        db_table = 'User'
        verbose_name = 'User'
        verbose_name_plural = 'Users' 
        
