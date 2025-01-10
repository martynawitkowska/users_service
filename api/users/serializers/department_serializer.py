from rest_framework import serializers

from users.models import Department

from .organization_serializer import OrganizationSerializer


class DepartmentSerializer(serializers.ModelSerializer):
	organization = OrganizationSerializer(read_only=True)

	class Meta:
		model = Department
		fields = ['id', 'name', 'organization', 'created_at', 'updated_at']
