from functools import wraps
from django.core.cache import cache as django_cache

def cache(key: str =None , timeout: int =0 )-> any: 
    def _decorator(viewfunc):   
        @wraps(viewfunc)
        def _wrappedView(request, *args, **kwargs): 
            if key is None: 
                raise AttributeError("Cache key is not provided")

            cached_data = django_cache.get(key) 
            if cached_data is not None:     
                print("--->>>>>", cached_data)        
                return cached_data 

            # Call the view function with the request object and other arguments
            response = viewfunc(request, *args, **kwargs)  

            # Cache the response with the specified key and timeout using django_cache
            django_cache.set(key, response, timeout) 
            return response 
        
        return _wrappedView       
    
    return _decorator 

