from django.shortcuts import redirect

class LoginAuthentication:

    def __init__(self , get_response):
        self.get_response =  get_response

    def __call__(self , request):

        excluded_exact = ['/auth/login/', '/auth/logout/']
        excluded_prefix = ['/api/']
        
        path = request.path
        if not request.user.is_authenticated:

            if not any(path.startswith(p) for p in excluded_prefix) and path not in excluded_exact:
                    return redirect('auth_login_basic')
        response = self.get_response(request)

        return response
