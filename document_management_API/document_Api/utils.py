import jwt
from datetime import datetime, timedelta  

from django.http import JsonResponse 

from django.contrib.auth.models import User
from document_management_API.settings import SECRET_KEY


def generate_jwt_token(user_id):
    expiry_time = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
    payload = {'user_id': user_id, 'exp': expiry_time}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')



class JWTAuthMixin: 
    
    def validate_jwt_token(self, token):    
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256') 
            return decoded_token 
        
        except jwt.ExpiredSignatureError:
            raise Exception('Expired token') 
        except jwt.InvalidTokenError:
            raise Exception('Invalid token') 
        

    def dispatch(self, request, *args, **kwargs): 
        
        try:  
            token = request.headers.get('Authorization')
            token = token.split('Bearer ')[-1]    
            decoded_token = self.validate_jwt_token(token)   
            print(decoded_token) 
        except AttributeError: 
            return JsonResponse({'error': "token missing"}, status=401)
        
        try: 
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)