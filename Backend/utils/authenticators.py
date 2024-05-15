from datetime import datetime, timedelta
from rest_framework.response import Response
from django.conf import settings
import jwt

def generate_jwt_token(user_id):
    try:
        # Define payload (claims) for the JWT token
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
        }

        # Generate JWT token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        return token
    
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)
