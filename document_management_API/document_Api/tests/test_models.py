from django.test import TestCase

from ..models import Document 

class DocumentModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
       Document.objects.create(name='aadhar.png',size=1023,
                               description='related to personal',
                               content_type='image/png') 
    

    def test_name_max_length(self):
        document = Document.objects.get(name='aadhar.png') 
        max_length = document._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)

    def test_content_type_default_is_none(self):
        document = Document.objects.get(name='aadhar.png')  
        default = document._meta.get_field('content_type').default
        self.assertIsNone(default)
