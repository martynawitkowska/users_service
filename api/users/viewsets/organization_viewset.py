from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import Organization
from users.serializers import OrganizationSerializer


@extend_schema_view(
	retrieve=extend_schema(
		parameters=[
			OpenApiParameter(
				name='id',
				type=OpenApiTypes.INT,
				location=OpenApiParameter.PATH,
				required=True,
				description='ID of the organization to retrieve',
			)
		]
	)
)
class OrganizationViewSet(viewsets.ModelViewSet):
	serializer_class = OrganizationSerializer
	permission_classes = [IsAuthenticated]
	http_method_names = ['get', 'post']
	lookup_field = 'id'

	def get_queryset(self):
		return Organization.objects.filter(tenant=self.request.tenant)
