from django.http import HttpResponseForbidden

class BlockAdminForUnauthorizedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not (
            request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
        ):
            return HttpResponseForbidden("403 Forbidden: You don't have access to admin panel.")

        return self.get_response(request)
