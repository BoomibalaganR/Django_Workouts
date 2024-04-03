from django.test import TestCase 

from author.models import User
from ..models import Post  
 
class PostModelTestCase(TestCase): 
    
    def setUp(self) -> None:
        self.boomi = User.objects.create(username='boomibalagan',password='1234')
    
    def test_post_creation(self): 
        
        post_instance = Post.objects.create(title='crimeNews',content="related to crime", author= self.boomi) 
        self.assertEqual(post_instance.title, 'crimeNews') 
        self.assertEqual(post_instance.content, 'related to crime') 
        self.assertEqual(post_instance.author.username, 'boomibalagan') 

       


    
    
        
        
    
    
        


