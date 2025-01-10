import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from users.models import Customer, Tenant
from users.serializers import CustomerSerializer


@pytest.mark.django_db
def test_customer_retrieve(api_client, user, department):
	api_client.force_authenticate(user=user)
	api_client.credentials(HTTP_X_TENANT_ID=user.tenant.id)

	customer = Customer.objects.create(user=user, department=department)

	url = reverse('users:customer-detail', args=[customer.id])
	response = api_client.get(url)

	expected_data = CustomerSerializer(customer).data

	assert response.status_code == status.HTTP_200_OK
	assert response.data == expected_data


@pytest.mark.django_db
def test_customer_retrieve_unauthenticated(api_client, user, department):
	customer = Customer.objects.create(user=user, department=department)

	url = reverse('users:customer-detail', args=[customer.id])
	response = api_client.get(url)

	assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_customer_list(api_client, user, user2, department, department2):
	api_client.force_authenticate(user=user)
	api_client.credentials(HTTP_X_TENANT_ID=user.tenant.id)

	customer1 = Customer.objects.create(user=user, department=department)
	customer2 = Customer.objects.create(user=user2, department=department2)

	url = reverse('users:customer-list')
	response = api_client.get(url)

	expected_data = CustomerSerializer([customer1], many=True).data

	assert response.status_code == status.HTTP_200_OK
	assert response.data == expected_data


@pytest.mark.django_db
def test_tenant_retrieve_success(api_client, user, tenant):
	api_client.force_authenticate(user=user)
	api_client.credentials(HTTP_X_TENANT_ID=user.tenant.id)

	url = reverse('users:tenant-detail', kwargs={'id': tenant.id})
	response = api_client.get(url)
	assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_tenant_retrieve_not_found(api_client, user):
	api_client.force_authenticate(user=user)
	api_client.credentials(HTTP_X_TENANT_ID=user.tenant.id)

	url = reverse('users:tenant-detail', kwargs={'id': 9999})
	response = api_client.get(url)
	assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_tenant_create_success(api_client, user):
	api_client.force_authenticate(user=user)
	url = reverse('users:tenant-list')

	payload = {'name': 'New Tenant', 'domain': 'newtenant.com'}
	response = api_client.post(url, data=payload, format='json')

	assert response.status_code == status.HTTP_201_CREATED
	assert Tenant.objects.filter(name='New Tenant').exists()


@pytest.mark.django_db
def test_tenant_create_unauthorized(api_client):
	url = reverse('users:tenant-list')
	payload = {'name': 'New Tenant', 'domain': 'newtenant.com'}
	response = api_client.post(url, data=payload, format='json')
	assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_organization_viewset_retrieve_authenticated(api_client, user, organization):
	api_client.force_authenticate(user=user)
	api_client.credentials(HTTP_X_TENANT_ID=user.tenant.id)

	url = reverse('users:organization-detail', kwargs={'id': organization.id})

	response = api_client.get(url)
	assert response.status_code == status.HTTP_200_OK
	assert response.data['name'] == 'Test Organization'


@pytest.mark.django_db
def test_organization_viewset_retrieve_unauthenticated(api_client, user, organization):
	url = reverse('users:organization-detail', kwargs={'id': organization.id})

	response = api_client.get(url)

	assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_organization_viewset_post_authenticated(api_client, user):
	api_client.force_authenticate(user=user)
	api_client.credentials(HTTP_X_TENANT_ID=user.tenant.id)

	data = {'name': 'New Organization', 'tenant': user.tenant.id}
	url = reverse('users:organization-list')

	response = api_client.post(url, data)

	assert response.status_code == status.HTTP_201_CREATED
	assert response.data['name'] == 'New Organization'


@pytest.mark.django_db
def test_organization_viewset_post_unauthenticated(api_client):
	tenant = Tenant.objects.create(name='Test Tenant')

	data = {'name': 'New Organization'}
	url = reverse('users:organization-list')
	response = api_client.post(url, data)

	assert response.status_code == status.HTTP_403_FORBIDDEN
