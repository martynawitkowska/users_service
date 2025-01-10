from rest_framework import serializers

from users.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ['id', 'name', 'tenant', 'created_at', 'updated_at']
