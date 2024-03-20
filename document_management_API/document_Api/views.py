from django.db.models.base import Model as Model
from django.http import JsonResponse
                          
from django.core.serializers import serialize
from django.views.generic import (DetailView, 
                                  CreateView,
                                  View, 
                                  UpdateView,
                                  ListView)  

import json
from .models import Document
from .forms import DocumentUploadForm,DocumentUpdateForm
from document_management_API.settings import storage   
from .utils import generate_jwt_token,JWTAuthMixin 




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
        
        return JsonResponse({'success': True, 'message': 'Data saved successfully'})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'message': 'Form validation failed'}, status=400)
   

# get all documents
class DocumentListView(JWTAuthMixin, ListView):
    model = Document
    
    def get(self, request, *args, **kwargs):
        # Retrieve queryset
        queryset = self.get_queryset()
        
        if len(queryset)== 0: 
            return JsonResponse({'message': 'no data available'})

        # Serialize queryset to JSON
        serialized_data = serialize('json', queryset)
        
        list_of_file = [file['fields'] for file in json.loads(serialized_data)]
        
        # Return JSON response
        return JsonResponse( {'data':list_of_file}, status=200, safe=False)
    
    

# get  document detail  using file name
class DocumentDetailView(JWTAuthMixin, DetailView): 
    model = Document 

    def get(self, request, *args, **kwargs): 
        
        # Retrieve object by file name
        pk = kwargs.get('name') 
        
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
            return JsonResponse({'error':'false','data':data})
        
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
                print("--->>>>>>>",instance, update_data)
                
                form = self.form_class(update_data, instance=instance)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'message': 'description updated successfully'})
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
