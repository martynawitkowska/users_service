from rest_framework.routers import DefaultRouter

from .viewsets import CustomerViewSet, DepartmentViewSet, OrganizationViewSet, TenantViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = router.urls
