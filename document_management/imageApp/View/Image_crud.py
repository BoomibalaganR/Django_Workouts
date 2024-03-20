from django.db.models.base import Model as Model
from django.http import (HttpRequest, HttpResponse,
                         JsonResponse)

from django.views.generic import (ListView,
                                  DeleteView, 
                                  DetailView, 
                                  FormView,View) 
from django.shortcuts import get_object_or_404 
from django.urls import reverse_lazy

from ..models import ImageMetadata
from ..forms import ImageUploadForm
from document_management.settings import storage  
import requests


# upload new image using class based 
class ImageCreateView(FormView):
    
    form_class = ImageUploadForm
    template_name = 'create-page.html'   
    success_url = reverse_lazy('all-images')
    
    def form_valid(self, form): 
    
        uploaded_image = form.cleaned_data["image_file"]
        # make destination path
        destination_path = "images/" + uploaded_image.name 
         
        # check if filename already exit or not
        if ImageMetadata.objects.filter(name=uploaded_image.name).count() > 0:  
           
            return JsonResponse({"error": "yes", "message": "file name already exits"})  
            #response =  redirect(resolve_url("create-image")) 
            #return response
        
        # Upload image to Firebase Cloud Storage
        storage.child(destination_path).put(uploaded_image.read())
                
        # Save image metadata to MongoDB
        metadata = ImageMetadata(
            name=uploaded_image.name,
            size=uploaded_image.size / 1024,  
            content_type=uploaded_image.content_type, 
            storage_path = destination_path,
            url=storage.child(destination_path).get_url(token=None)
        )
        metadata.save()  
        return super().form_valid(form)


# get all images using class based
class ImageListView(ListView):
    model = ImageMetadata
    template_name = 'all_images.html'
    context_object_name = 'images' 


# get a image detail  
class ImageDetailView(DetailView): 
    model = ImageMetadata  
    template_name = 'display_single_image.html'
    context_object_name = 'image'  
    
    
    def get_object(self, queryset=None):
        # Retrieve the object using the name 
        name = self.kwargs.get('name')
        return get_object_or_404(self.get_queryset(), name=name)


# delete image using class based
class ImageDeleteView(DeleteView): 
    model = ImageMetadata   
    success_url = reverse_lazy('all-images') 
    
    
    def post(self, request,  *args, **kwargs) -> HttpResponse: 
        image_instance = self.get_object() 
        storage.delete(image_instance.storage_path,token=None)
        return super().post(request, *args, **kwargs) 


# download the image 
class ImageDownloadView(View):  
    
    
    def get(self, request, pk): 
    
        # get image_instance from mongoDb using image id
        image_instance= ImageMetadata.objects.get(id=pk)   
    
        # get image storage location from the image_instance
        image_path = image_instance.storage_path 
    
        # get url from Firebase Cloud Storage 
        download_url = storage.child(image_path).get_url(token=None)

        # make GET request to download url
        response = requests.get(download_url)

        # Check if the request was successful
        if response.status_code == 200:
            content_type = response.headers['Content-Type'] 
            
            # make django httpResponse, set content and conten_type
            response = HttpResponse(response.content, content_type=content_type) 
            
            # set the value of content disposition is 'attachment'
            response['Content-Disposition'] = f'attachment; filename="{image_instance.name}"'
            
            return response 
        else:
            return HttpResponse("image not downloaded..")

   
        
    
 
        

    