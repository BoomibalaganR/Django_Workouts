from django.test import TestCase  
from django.urls import reverse  

from rest_framework import status

from author.models import User 
from post. models import Post 
from .models import Comment 
from urllib.parse import urlencode


import json


class CreateCommentViewTestCase(TestCase): 
    
    def setUp(self) -> None:
               
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)   
        
        self.valid_payload= {
            'post_id': str(self.post1._id), 
            'content': 'interesting post'
        } 
        self.payload_with_invalid_post_id={
            'post_id': '550128c3fde9696dca7eba24', 
            'content': 'its bad comment'
        } 
        self.payload_without_content={
            'post_id': str(self.post1._id)
        } 
        self.empty_payload={}
    
    
    def test_create_comment_on_valid_post_id(self): 
        
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.valid_payload), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    
    def test_create_comment_on_invalid_post_id(self): 
        
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.payload_with_invalid_post_id), 
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_create_comment_without_content(self): 
        
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.payload_without_content), 
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_comment_empty_payload(self): 
        
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.empty_payload), 
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class UpdateCommentViewTestCase(TestCase): 
    
    def setUp(self):
                
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)   
        # for i in range(1):  
        #     content = f"commented by {self.suriya.username}"
        #     self.comment1 = Comment.objects.create(post = self.post1, user = self.suriya, content=content)
        # print(Comment.objects.all())   
        content = f"commented by {self.suriya.username}"
        self.comment1 = Comment.objects.create(post = self.post1, user = self.suriya, content=content)
       
        
        self.valid_payload={
                            'content': f'updated comment by {self.suriya.username}'
                            }
        self.invalid_payload={'content': ' '}  
        
    
    
    def test_update_comment_with_valid_payload_with_valid_cmt_id(self): 
        
        url = reverse('comment-rud', kwargs={'comment_id': str(self.comment1._id)})  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.put(path=url,
                         data=json.dumps(self.valid_payload), 
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_update_comment_with_invalid_cmt_id(self): 
        
        url = reverse('comment-rud', kwargs={'comment_id': '550128c3fde9696dca7eba24'})  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.put(path=url,
                         data=json.dumps(self.valid_payload), 
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_update_comment_with_empty_content(self): 
        
        url = reverse('comment-rud', kwargs={'comment_id': str(self.comment1._id)})  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.put(path=url,
                         data=json.dumps(self.invalid_payload), 
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class DeleteCommentViewTestCase(TestCase): 
    
    def setUp(self):
                
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)   
     
        content = f"commented by {self.suriya.username}"
        self.comment1 = Comment.objects.create(post = self.post1, user = self.suriya, content=content)
       
       
    
    def test_delete_comment_with_valid_payload_with_valid_cmt_id(self): 
        
        url = reverse('comment-rud', kwargs={'comment_id': str(self.comment1._id)})  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.delete(path=url,
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)     

    
    def test_delete_comment_with_not_exit_cmt_id(self): 
        
        url = reverse('comment-rud', kwargs={'comment_id': '550128c3fde9696dca7eba24'})  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.delete(path=url,
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_with_invalid_cmt_id(self): 
        
        url = reverse('comment-rud', kwargs={'comment_id': '550128c3fde9696dca7eba'})  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.delete(path=url,
                         content_type='application/json')  
        print('\nresponse::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    


class GetCommentViewTestCase(TestCase): 
    
    def setUp(self):
                
        self.rolex = User.objects.create(username='rolex',password='12345') 
        self.suriya = User.objects.create(username='suriya',password='12346') 
        
        self.post1= Post.objects.create(title='crime',
                                        content='related to crime',
                                        author=self.rolex) 
        self.post2= Post.objects.create(title='cine',
                                        content='related to cinema',
                                        author=self.suriya)   
        for i in range(2):  
            content = f"commented by {self.suriya.username} on rolex post"
            Comment.objects.create(post = self.post1, user = self.suriya, content=content)   
        
        for i in range(2):  
            content = f"commented by {self.rolex.username} on rolex post"
            Comment.objects.create(post = self.post1, user = self.rolex, content=content) 
            

        

    def test_get_all_comment_by_valid_post_id(self):  
        
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url)  
        
        query_params = {'post_id': str(self.post1._id)}
        query_string = urlencode(query_params)
        
        response = self.client.get(path=url, QUERY_STRING=query_string)   
        
        print('response::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    
    def test_get_all_comment_by_invalid_post_id(self):  
        print("invalid post id")
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url)  
        
        query_params = {'post_id': '550128c3fde9696dca7eba24'}
        query_string = urlencode(query_params)
        
        response = self.client.get(path=url, QUERY_STRING=query_string)   
        
        print('response::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
        

    def test_get_all_comment_by_without_post_id(self):  
        print("without post id")
        url = reverse('comment-create-list')  
        print("\n\n---->>>>>>>",url)  
        
        # query_params = {'post_id': '550128c3fde9696dca7eba24'}
        # query_string = urlencode(query_params)
        
        response = self.client.get(path=url)   
        
        print('response::',response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    
    