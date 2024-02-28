from django.shortcuts import render
from django.http import (HttpResponse,
                         JsonResponse) 

from .models import ImageMetadata
from document_management.settings import storage 

import requests



def get_All_images(request):  
     
    # get image details from mongoDB
    images_details = ImageMetadata.objects.all()
    
    return render(request, 'all_images.html', {'images': images_details} )
    


def upload_image(request): 
    
    if request.method == 'POST' and request.FILES['image']: 
        
        # get image from request
        uploaded_image = request.FILES['image']

        # make destination path
        destination_path = "images/" + uploaded_image.name 
         
        # check if filename already exit or not
        if ImageMetadata.objects.filter(name=uploaded_image.name).count() > 0: 
            return JsonResponse({"error": "yes", "message": "file name already exits"}) 
        
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

        # success message
        return HttpResponse("<h1>Image uploaded successfully.</h1>")


def delete_image(request, image_id):  
    
    try:
        # Get the image instance based on image_id
        image_instance = ImageMetadata.objects.get(id=image_id) 
        
        # first, delete the image instance in the mongodb
        image_instance.delete()

        # second, delete actual file from the storage (firebase)
        storage.delete(image_instance.storage_path,token=None)

        return HttpResponse("<h2>Image deleted successfully.</h2>") 
    
    except ImageMetadata.DoesNotExist:
        return HttpResponse("Image not found.", status=404) 
    
    

def download_image(request, image_id): 
    
    # get image_instance from mongoDb using image id
    image_instance= ImageMetadata.objects.get(id=image_id)   
    
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
