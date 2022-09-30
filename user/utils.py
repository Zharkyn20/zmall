from django.contrib.auth import get_user_model

User = get_user_model()

def get_token_in_headers(request):
    token = request.headers.get('Authorization')
    return token
