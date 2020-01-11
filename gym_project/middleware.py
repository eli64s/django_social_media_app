import re
from django.conf import settings 
from django.shortcuts import redirect 
from djang.contrib.auth import logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_ags, view_kwags):
        assert hasattr(request, 'user') # Checks if request.user exists 
        path = request.path_info.lstrip('/')
        print(path)
        
        if not request.user.is_authenticated: 
            if not any(url.match(path) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if path == 'account/logout/':
            logout(request)

        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)

        elif request.user.is_authenticated or url_is_exempt:
            return None
        # View a page as a non-logged in user
        else:
            return redirect(settings.LOGIN_URL)