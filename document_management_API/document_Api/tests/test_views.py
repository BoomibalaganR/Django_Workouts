from django.test import TestCase,Client
from django.urls import reverse 

from ..models import Document  
from ..utils import generate_jwt_token

class DocumentListViewTest(TestCase): 
    
    @classmethod
    def setUpTestData(cls):
        # Create 13 documents
        number_of_document = 13
        
        for doc_id in range(number_of_document):
            Document.objects.create(
                name=f'document{doc_id}',size=doc_id+100
            ) 
        print("setup the data")
        print(Document.objects.all().__dict__) 
    def setUp(self):
        self.client = Client() 
        self.token = generate_jwt_token("boomi")
    
    def test_view_url_exists_at_desired_location(self): 
        print("test the correct url location") 
        
        headers ={'HTTP_AUTHORIZATION': f'Bearer {self.token}'} 
        url = reverse('all-document')
        response = self.client.get(url, **headers)
        
        self.assertEqual(response.status_code, 200) 
    
    def test_view_url_acess_by_doc_name(self):
        print("test get document by name")  
        
        headers ={'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        url = reverse('all-document')+'document1/'
        response = self.client.get(url, **headers) 
        
        print("---->>>>>",response.status_code)
        self.assertEqual(response.status_code, 200)  



class DocumentDetailViewTestCase(TestCase):
    def setUp(self):
        self.document = Document.objects.create(name='test_document.txt', size=1234) 
        self.client = Client() 
        self.token = generate_jwt_token("boomi")

    def test_document_detail_view(self): 
        headers ={'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        url = reverse('single-document', kwargs={'name': self.document.name})
        response = self.client.get(url,**headers)

        # verify the response code
        self.assertEqual(response.status_code, 200)


    def test_document_detail_view_not_found(self): 
        headers ={'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        url = reverse('single-document', kwargs={'name': 'unKnown_document.txt'})
        response = self.client.get(url, **headers)

        # verify the response code
        self.assertEqual(response.status_code, 404)
   

