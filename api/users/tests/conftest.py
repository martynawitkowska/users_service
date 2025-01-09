import pytest

from users.models import Department, Organization, Tenant


@pytest.fixture
def tenant():
    """Fixture for creating a tenant."""
    return Tenant.objects.create(name="Test Tenant", domain="test.com")


@pytest.fixture
def organization(tenant):
    """Fixture for creating an organization linked to a tenant."""
    return Organization.objects.create(name="Test Organization", tenant=tenant)


@pytest.fixture
def department(organization):
    """Fixture for creating a department linked to an organization."""
    return Department.objects.create(name="Test Department", organization=organization)
