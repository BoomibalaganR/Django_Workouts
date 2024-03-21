from django.db.models.base import Model as Model
from django.http import JsonResponse
                          
from django.core.serializers import serialize
from django.views.generic import (DetailView, 
                                  CreateView,
                                  View, 
                                  UpdateView,
                                  ListView)   

from django.views.decorators.cache import cache_page 
from django.core.cache import cache as django_cache
from django.utils.decorators import method_decorator

import json
from .models import Document
from .forms import DocumentUploadForm,DocumentUpdateForm
from document_management_API.settings import storage   
from .utils import generate_jwt_token,JWTAuthMixin  
from .decorators import cache

GET_ALL_RECORDS_CACHE_KEY = 'all_records'
GET_SINGLE_RECORD_CACHE_KEY_PREFIX = 'single_record_'


# upload new document using class based 
class DocumentCreateView(JWTAuthMixin, CreateView):
    
    form_class = DocumentUploadForm  
    model = Document 
    
    
    def form_valid(self, form):  
        
        # get file from cleaned data dictionary    
        file_obj = form.cleaned_data["files"] 
    
        # check if filename already exit or not
        if self.model.objects.filter(name=file_obj.name).count() > 0:         
            return JsonResponse({"error": "true", "message": "file already exits"},status=409)  

        # make destination path
        destination_path = "images/" + file_obj.name 
        
        # Upload file into Firebase Cloud Storage
        storage.child(destination_path).put(file_obj.read()) 
        
    
        # Get the form instance
        form_instance = form.save(commit=False)  
       
        
        form_instance.size = file_obj.size  
        form_instance.name = file_obj.name 
        form_instance.content_type = file_obj.content_type 
        form_instance.storage_path = destination_path
        form_instance.url=storage.child(destination_path).get_url(token=None)
        form.save()  
        
        # delete cache
        django_cache.delete(GET_ALL_RECORDS_CACHE_KEY)
        
        return JsonResponse({'success': True, 'message': 'Data saved successfully'}, status=200)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'message': 'Form validation failed'}, status=400)
   

# get all documents
class DocumentListView(JWTAuthMixin, ListView):
    model = Document

   # @cache(key='all-record',timeout=60)
    def get(self, request, *args, **kwargs): 
        
        cached_data =  django_cache.get(GET_ALL_RECORDS_CACHE_KEY)  
        if cached_data is not None: 
            return cached_data 
        
        # Retrieve queryset
        queryset = self.get_queryset() 
       
        print("------->>>>>>>>>","no cache available..") 
        
        if len(queryset)== 0: 
            return JsonResponse({'message': 'no data available'},status=404)

        # Serialize queryset to JSON
        serialized_data = serialize('json', queryset)
        
        list_of_file = [file['fields'] for file in json.loads(serialized_data)]
        
        # Return JSON response
        response =  JsonResponse( {'data':list_of_file}, status=200, safe=False)  
        
        # to save response in cache
        django_cache.set(GET_ALL_RECORDS_CACHE_KEY, response, timeout=60*2) 
        return response
    
    

# get  document detail  using file name
class DocumentDetailView(JWTAuthMixin, DetailView): 
    model = Document 

    
    def get(self, request, *args, **kwargs): 
        
        # Retrieve object by file name
        pk = kwargs.get('name') 
        print("---->>>>>>","no cache available")
        try:
            obj = self.model.objects.get(name=pk) 
    
            serialized_data = serialize('json',[obj])  
            data =  json.loads(serialized_data)[0]['fields']  

            return JsonResponse({'error':'false','data':data},status=200)
        
        except self.model.DoesNotExist:
            # file not found given name doesnot match
            return JsonResponse({'error': 'true' ,'message':'given file name not found'}, status=404)


# delete the documet using document name
class DocumentDeleteView(JWTAuthMixin, View): 
    
    def delete(self, request, *args, **kwargs):
        name = kwargs.get('name')  
        
        try:
            document = Document.objects.get(name=name)
            document.delete() 
            storage.delete(document.storage_path,token=None)   
            
            # delete cache
            django_cache.delete(GET_ALL_RECORDS_CACHE_KEY)
            
            return JsonResponse({'message': 'Document deleted successfully'}, status=200)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)


# download the document 
class DocumentDownloadView(JWTAuthMixin, DetailView):    
    model = Document

   
    def get(self, request, *args, **kwargs): 
        
        # Retrieve object by file name
        name = kwargs.get('name') 
        
        try:
            obj = self.model.objects.get(name=name) 
            data = {'url':obj.url}
            return JsonResponse({'error':'false','data':data},status=200)
        
        except self.model.DoesNotExist:
            # file not found given name doesnot match
            return JsonResponse({'error': 'true' ,'message':'given file name not found'}, status=404)

    
# update document using update class based view 
class DocumentUpdateView(JWTAuthMixin, UpdateView):   
        model = Document  
        form_class = DocumentUpdateForm
        
        def post(self, request, *args, **kwargs): 
            name = kwargs.get("name")
           
            try:
                instance = self.model.objects.get(name = name)  
                update_data = json.loads(request.body)

                form = self.form_class(update_data, instance=instance)
                if form.is_valid():
                    form.save()   
                    
                    # delete cache
                    django_cache.delete(GET_ALL_RECORDS_CACHE_KEY)
                    
                    return JsonResponse({'message': 'description updated successfully'},status=200)
                else:
                    return JsonResponse({'errors': form.errors}, status=400)
            except self.model.DoesNotExist:
                return JsonResponse({'error': 'Object not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500) 
            
            
class LoginAPIView(View):
    
    def post(self, request):
        # Retrieve username and password from request data 
        credential = json.loads(request.body)
        username = credential.get('username')
        password = credential.get('password')   
        
    
        if not username or not password:  
            return JsonResponse({'message': 'username and password Required'}, status=400)
       
        if username == 'boomi' and password == '1234' : 
            encoded_token = generate_jwt_token(username) 
            
            return JsonResponse({'error': 'false','token':encoded_token, 'data':{}}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=401)
