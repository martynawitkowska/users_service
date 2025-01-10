from django.core.exceptions import MiddlewareNotUsed, PermissionDenied
from django.urls import resolve

from .models import Tenant


class TenantMiddleware:
    """
    Middleware to identify the active tenant based on request headers, domain,
    or tokens.
    """
    EXEMPT_URL_NAMES = [
        'swagger',
        'openapi',
        'token_obtain_pair',
        'token_refresh'
    ]

    EXEMPT_POST_ONLY_URLS = ['tenant-list']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name

        if request.path.startswith('/admin/'):
            return self.get_response(request)

        if url_name in type(self).EXEMPT_URL_NAMES:
            return self.get_response(request)

        if url_name in type(self).EXEMPT_POST_ONLY_URLS and request.method == "POST":
            return self.get_response(request)


        tenant_id = request.headers.get('X-Tenant-ID')

        if not tenant_id:
            raise PermissionDenied("Tenant ID is required to access this resource.")

        try:
            tenant = Tenant.objects.get(id=tenant_id)
            request.tenant = tenant_id
        except Tenant.DoesNotExist:
            raise PermissionDenied(f"Invalid tenant: {tenant_id}")


        return self.get_response(request)