from unittest.mock import patch, Mock

import pytest
from users.middleware import TenantMiddleware
from users.models import Tenant
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import ResolverMatch
from django.urls.exceptions import Resolver404


@pytest.mark.django_db
def test_exempt_url_allows_request():
    get_response = Mock()
    middleware = TenantMiddleware(get_response)
    with patch("users.middleware.resolve") as mock_resolve:
        mock_resolve.return_value = ResolverMatch(
            func=None,
            args=(),
            kwargs={},
            url_name="swagger",
            app_names=[],
            namespaces=[],
        )
        request = RequestFactory().get("/swagger")

        response = middleware(request)

    get_response.assert_called_once_with(request)
    assert response == get_response.return_value


@pytest.mark.django_db
def test_missing_tenant_id_raises_permission_denied():
    get_response = Mock()
    middleware = TenantMiddleware(get_response)
    with patch("users.middleware.resolve") as mock_resolve:
        mock_resolve.return_value = ResolverMatch(
            func=None,
            args=(),
            kwargs={},
            url_name="some_view",
            app_names=[],
            namespaces=[],
        )
        request = RequestFactory().get("/")
        request.headers = {}

        with pytest.raises(PermissionDenied, match="Tenant ID is required to access this resource."):
            middleware(request)


@pytest.mark.django_db
def test_invalid_tenant_id_raises_permission_denied():
    get_response = Mock()
    middleware = TenantMiddleware(get_response)
    with patch("users.middleware.resolve") as mock_resolve:
        mock_resolve.return_value = ResolverMatch(
            func=None,
            args=(),
            kwargs={},
            url_name="some_view",
            app_names=[],
            namespaces=[],
        )
        request = RequestFactory().get("/")
        request.headers = {"X-Tenant-ID": "invalid-id"}
        with patch("users.middleware.Tenant.objects.get", side_effect=Tenant.DoesNotExist):
            with pytest.raises(PermissionDenied, match="Invalid tenant: invalid-id"):
                middleware(request)


@pytest.mark.django_db
def test_valid_tenant_allows_request():
    get_response = Mock()
    middleware = TenantMiddleware(get_response)
    with patch("users.middleware.resolve") as mock_resolve:
        mock_resolve.return_value = ResolverMatch(
            func=None,
            args=(),
            kwargs={},
            url_name="some_view",
            app_names=[],
            namespaces=[],
        )
        # Create a Tenant instance with the correct field
        tenant = Tenant.objects.create(name="Test Tenant")
        request = RequestFactory().get("/")
        request.headers = {"X-Tenant-ID": tenant.id}  # Use tenant.id if no tenant_id field exists
        with patch("users.middleware.Tenant.objects.get", return_value=tenant):
            response = middleware(request)

    get_response.assert_called_once_with(request)
    assert response == get_response.return_value
    assert request.tenant == tenant.id


@pytest.mark.django_db
def test_unresolvable_url_raises_resolver404():
    get_response = Mock()
    middleware = TenantMiddleware(get_response)
    with patch("users.middleware.resolve") as mock_resolve:
        mock_resolve.side_effect = Resolver404
        request = RequestFactory().get("/invalid-url")

        with pytest.raises(Resolver404):
            middleware(request)
