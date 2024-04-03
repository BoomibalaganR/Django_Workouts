from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication,JWTAuthentication
from rest_framework_simplejwt.tokens import Token  

from rest_framework_simplejwt.settings import api_settings 
from rest_framework_simplejwt.exceptions import InvalidToken


from bson import ObjectId

class CustomJWTAuthentication(JWTAuthentication): 
    
    def get_user(self, validated_token: Token): 
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM] 
            validated_token[api_settings.USER_ID_CLAIM] = ObjectId(user_id)
        except KeyError:
            raise InvalidToken(("Token contained no recognizable user identification"))

        return super().get_user(validated_token)