from .models import ImageMetadata
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.core.serializers import serialize

import hashlib 


def calculate_Etag(request, image_id=None): 
    
    if image_id is not None:
        # Calculate Etag for single image
        image_instance = ImageMetadata.objects.get(id=image_id) 
        
        # If no image found, generate an ETag based fixed value
        if image_instance is None:
            return hashlib.md5('no_images_found'.encode()).hexdigest() 
        
        # Extract relevant data from each image instance (for illustration, using image_metadata)
        serialized_object = serialize('json', [image_instance]) 

        # Concatenate the serialized representations into a single string
        content = "\n".join(serialized_object)

        # Calculate content hash
        etag = hashlib.md5(content.encode()).hexdigest()
 
        return etag

    # Calculate Etag for all images
    try:  
        image_instance = ImageMetadata.objects.all()  
       
        # Extract relevant data from each image instance (for illustration, using image_metadata)
        serialized_objects = [serialize('json', [image]) for image in image_instance]
        print("------->>>>>>>",serialized_objects)
        # Concatenate the serialized representations into a single string
        content = "\n".join(serialized_objects)

        # Calculate content hash
        etag = hashlib.md5(content.encode()).hexdigest()
 
        return etag

    except ObjectDoesNotExist:
         # If no images found, generate an ETag based fixed value
            return hashlib.md5('no_images_found'.encode()).hexdigest()
    


def calculate_last_modified(request, image_id=None):
    
    if image_id is not None:
        # Calculate last modified time for a single product
        try:
            images = ImageMetadata.objects.get(pk=image_id)
            return images.last_modified
        except ImageMetadata.DoesNotExist:
            return timezone.now()


    # Calculate last modified time for all products
    try:
        latest_image = ImageMetadata.objects.latest('last_modified') 
        latest_updated_at = latest_image.last_modified
    except ObjectDoesNotExist:
         return timezone.now()
    return latest_updated_at