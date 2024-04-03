from django.test import TestCase  
from django.urls import reverse  

from rest_framework import status 
import json 

from .models import User

class CreateUserViewTestCase(TestCase): 
    
    def setUp(self):
        
        self.valid_payload = { 
                      'username': 'boomi', 
                      'password': 'abc123'
                      } 
        self.invalid_payload = {
                        'username': "", 
                        'password': ''
                        } 
        self.empty_payload={} 
        
    
    def test_create_user_with_valid_payload(self): 
        url = reverse('user-create')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.valid_payload), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_user_with_invalid_payload(self): 
        url = reverse('user-create')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.invalid_payload), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
     
    def test_create_user_with_empty_payload(self): 
        url = reverse('user-create')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.empty_payload), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       


from django.contrib.auth.hashers import make_password
class LoginUserViewTestCase(TestCase): 
    
    def setUp(self) -> None: 
        self.rolex = User.objects.create_user(username='rolex',password='abc123') 
        self.suriya = User.objects.create_user(username='suriya',password='abc123') 
        
        self.valid_payload = { 
                      'username': 'rolex', 
                      'password': 'abc123'
                      } 
        self.invalid_payload = {
                        'username': "", 
                        'password': ''
                        } 
        self.invalid_username={
            'username': 'boomi', 
            'password': '0029'
        }  
    
    def test_user_login_with_valid_payload(self): 
        
        url = reverse('user-login')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.valid_payload), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_user_login_with_invalid_payload(self): 
        
        url = reverse('user-login')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.invalid_payload), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_invalid_username(self): 
        
        url = reverse('user-login')  
        print("\n\n---->>>>>>>",url) 
        
        response = self.client.post(path=url,
                         data=json.dumps(self.invalid_username), 
                         content_type='application/json')  
        print("\nresponse::",response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)