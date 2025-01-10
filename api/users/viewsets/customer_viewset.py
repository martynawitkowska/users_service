from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import Customer
from users.serializers import CustomerSerializer


@extend_schema_view(
	retrieve=extend_schema(
		parameters=[
			OpenApiParameter(
				name='id',
				type=OpenApiTypes.INT,
				location=OpenApiParameter.PATH,
				required=True,
				description='ID of the customer to retrieve',
			)
		]
	)
)
class CustomerViewSet(viewsets.ModelViewSet):
	serializer_class = CustomerSerializer
	permission_classes = [IsAuthenticated]
	lookup_field = 'id'
	http_method_names = ['get', 'post']

	def get_queryset(self):
		return Customer.objects.filter(department__organization__tenant=self.request.tenant)
