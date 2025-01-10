from rest_framework import serializers

from users.models import Customer
from .organization_serializer import OrganizationSerializer
from .user_serializer import UserReadSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'organization', 'created_at', 'updated_at']
