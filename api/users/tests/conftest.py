import pytest
from rest_framework.test import APIClient

from users.models import Department, Organization, Tenant, Customer


@pytest.fixture
def tenant():
    """Fixture for creating a tenant."""
    return Tenant.objects.create(name="Test Tenant", domain="test.com")


@pytest.fixture
def tenant2():
    """Fixture for creating a tenant."""
    return Tenant.objects.create(name="Test Tenant 2", domain="test2.com")


@pytest.fixture
def organization(tenant):
    """Fixture for creating an organization linked to a tenant."""
    return Organization.objects.create(name="Test Organization", tenant=tenant)


@pytest.fixture
def organization2(tenant2):
    """Fixture for creating an organization linked to a tenant."""
    return Organization.objects.create(name="Test Organization2", tenant=tenant2)


@pytest.fixture
def department(organization):
    """Fixture for creating a department linked to an organization."""
    return Department.objects.create(name="Test Department", organization=organization)


@pytest.fixture
def department2(organization2):
    """Fixture for creating a department linked to an organization."""
    return Department.objects.create(name="Test Department2", organization=organization2)


@pytest.fixture
def user(django_user_model, tenant):
    return django_user_model.objects.create_user(email="testuser@example.com", password="securepassword", tenant=tenant)


@pytest.fixture
def user2(django_user_model, tenant2):
    return django_user_model.objects.create_user(email="testuser2@example.com", password="securepassword", tenant=tenant2)


@pytest.fixture
def customer(user, department):
    """Fixture for creating a customer."""
    return Customer.objects.create(user=user, department=department)


@pytest.fixture
def api_client():
    return APIClient()
