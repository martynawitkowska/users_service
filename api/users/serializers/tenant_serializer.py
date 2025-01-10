from rest_framework import serializers

from users.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tenant
		fields = ['id', 'name', 'domain', 'created_at', 'updated_at']
