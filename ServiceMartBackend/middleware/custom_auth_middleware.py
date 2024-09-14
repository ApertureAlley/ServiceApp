from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import jwt
import pdb
from django.conf import settings
from User.models import CustomUser

class CustomAuthenticationMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        bypass_paths = {
            '/api/users/create': ['POST'],
            '/api/login': ['POST'],
            '/admin': ['GET', 'PUT', 'POST', 'PATCH', 'DELETE'],
            '/api/users/send_otp': ['POST'],
            '/api/users/verify_otp': ['POST']
        }  
        if any(request.path.startswith(path) and request.method in methods for path, methods in bypass_paths.items()):
            return self.get_response(request)

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header:
            try:
                # token = auth_header.split()[1]
                token = auth_header
                decoded_payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )
                user_id = decoded_payload.get('user_id')

                try:
                    user = CustomUser.objects.get(id=user_id)
                    request.custom_user = user
                except CustomUser.DoesNotExist:
                    return JsonResponse({"detail": "User not found.", "code": "user_not_found"}, status=404)

            except jwt.ExpiredSignatureError:
                return JsonResponse({"detail": "Token has expired. Please obtain a new token."}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"detail": "Invalid token."}, status=401)
        else:
            return JsonResponse({"detail": "Authorization header missing."}, status=401)

        return self.get_response(request)