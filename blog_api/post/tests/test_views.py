from django.test import TestCase 
from django.urls import reverse 

from rest_framework import status

from author.models import User
from ..models import Post  
import json


class PostListViewTestCase(TestCase): 
    def setUp(self) -> None:
        
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)  
    
    
    def test_get_all_post_with_valid_author(self):  
        url = reverse('post-read-create') 
        print("\n\n ------>>>>>>",url)
        response = self.client.get(path=url, content_type='application/json')
        print("response::", response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class PostCreateViewTestCase(TestCase): 
    
    def setUp(self) -> None:
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346')    
        
        self.valid_payload = {
            'title':'crimeNews', 
            'content': 'related to crime', 
        }   
        
        self.invalid_payload = {
            'title':'crimeNews', 
            #'content': 'related to crime',  
        } 
        
    
    def test_create_valid_post(self):
        print("\n\n------->>>>>", json.dumps(self.valid_payload), reverse('post-read-create'))
        response = self.client.post(reverse('post-read-create'),
                                    data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        
        print('response:::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        
        
    def test_create_invalid_post(self):
        print("\n\n------->>>>>", json.dumps(self.invalid_payload), reverse('post-read-create')) 
        
        response = self.client.post(reverse('post-read-create'),
                                    data=json.dumps(self.invalid_payload),
                                    content_type='application/json')  
        
        print('response:::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        


class PostDetailViewTestCase(TestCase): 
    
    def setUp(self) -> None:
        
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)  
    
    
    def test_post_detail_get_by_valid_id(self): 
        
        url = reverse('post-rud', kwargs={'post_id': str(self.post1._id)})   
        print("\n\n----->>>>>>>>",url)
        response = self.client.get(url)
        print("error::",response.content.decode())
        return self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_post_detail_get_by_invalid_id(self): 
        
        url = reverse('post-rud', kwargs={'post_id': '550128c3fde9696dca7eba24'})   
        print("\n\n----->>>>>>>>",url)
        response = self.client.get(url)
        print("error::",response.content.decode())
        return self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    
class PostUpdateViewTestCase(TestCase): 
    
    def setUp(self):
        
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)  
        
        
        self.valid_payload={'title': 'drugs', 
                            #'content': 'related to drugs', 
                            }   
        self.invalid_payload = {}
         
    
    def test_update_post_with_valid_payload(self): 
        
        url = reverse('post-rud', kwargs={'post_id': self.post1._id})  
        print('\n\n----->>>>>>>>',url)
        response = self.client.patch(url, 
                        data=json.dumps(self.valid_payload), 
                        content_type='application/json' )  
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
    
        
    def test_update_post_with_invalid_payload(self): 
        
        url = reverse('post-rud', kwargs={'post_id':'550128c3fde9696dca7eba24'})  
        print('\n\n----->>>>>',url)
        response = self.client.patch(url, 
                        data=json.dumps(self.invalid_payload), 
                        content_type='application/json' )  
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   
        


class PostDeleteViewTestCase(TestCase): 
    
    def setUp(self) -> None:
        
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)  
    
    
    def test_delete_post_with_valid_id(self):  
        
        url =reverse('post-rud',kwargs={'post_id': self.post1._id})  
        response = self.client.delete(path=url, 
                        content_type='application/json') 

        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)      
        

    def test_delete_post_with_invalid_id(self): 
        url = reverse('post-rud', kwargs={'post_id':'550128c3fde9696dca7eba24'})  
        print(url)
        response = self.client.delete(path= url, content_type='application/json' )  
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   
        