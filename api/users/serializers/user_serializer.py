from django.contrib.auth import get_user_model
from rest_framework import serializers

CustomUser = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = CustomUser
		fields = ['email', 'first_name', 'last_name', 'password', 'tenant']

	def create(self, validated_data):
		return CustomUser.objects.create_user(**validated_data)


class UserReadSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ['id', 'email', 'first_name', 'last_name', 'tenant']
