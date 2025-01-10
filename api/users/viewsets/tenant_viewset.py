from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import Tenant
from users.serializers import TenantSerializer


@extend_schema_view(
	retrieve=extend_schema(
		parameters=[
			OpenApiParameter(
				name='id',
				type=OpenApiTypes.INT,
				location=OpenApiParameter.PATH,
				required=True,
				description='ID of the tenant to retrieve',
			),
		]
	)
)
class TenantViewSet(viewsets.ModelViewSet):
	serializer_class = TenantSerializer
	permission_classes = [IsAuthenticated]
	lookup_field = 'id'
	http_method_names = ['get', 'post']

	def get_queryset(self):
		return Tenant.objects.filter(id=self.request.tenant)
