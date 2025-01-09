import pytest
from users.models import Department, Organization, Tenant
from django.db.utils import IntegrityError
from django.utils.timezone import now
from freezegun import freeze_time


@pytest.mark.django_db
def test_create_user_with_email(django_user_model):
    user = django_user_model.objects.create_user(email="test@example.com", password="password123")
    assert user.email == "test@example.com"
    assert user.check_password("password123")


@pytest.mark.django_db
def test_user_requires_unique_email(django_user_model):
    django_user_model.objects.create_user(email="unique@example.com", password="password123")
    with pytest.raises(IntegrityError):
        django_user_model.objects.create_user(email="unique@example.com", password="password123")


@pytest.mark.django_db
def test_str_representation(django_user_model):
    user = django_user_model.objects.create_user(email="test@example.com", password="password123")
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_user_with_tenant(django_user_model, tenant):
    user = django_user_model.objects.create_user(email="test@example.com", password="password123", tenant=tenant)
    assert user.tenant == tenant


@pytest.mark.django_db
def test_user_with_organization(django_user_model, organization):
    user = django_user_model.objects.create_user(email="test@example.com", password="password123",
                                                 organization=organization)
    assert user.organization == organization


@pytest.mark.django_db
def test_user_with_department(django_user_model, department):
    user = django_user_model.objects.create_user(email="test@example.com", password="password123",
                                                 department=department)
    assert user.department == department


@pytest.mark.django_db
def test_user_is_admin_flags(django_user_model):
    user = django_user_model.objects.create_user(
        email="admin@example.com",
        password="password123",
        is_tenant_admin=True,
        is_organization_admin=True,
        is_department_admin=True,
    )
    assert user.is_tenant_admin is True
    assert user.is_organization_admin is True
    assert user.is_department_admin is True


@pytest.mark.django_db
@freeze_time("2023-11-01 12:00:00")
def test_user_update_timestamp_freeze_time(django_user_model):
    user = django_user_model.objects.create_user(email="test@example.com", password="password123")
    original_updated_at = user.updated_at
    assert original_updated_at == now()

    with freeze_time("2023-11-01 13:00:00"):
        user.email = "updated_email@example.com"
        user.save()
        assert user.updated_at > original_updated_at
        assert user.updated_at == now()

@pytest.mark.django_db
def test_create_user_without_email_raises_error(django_user_model):
    with pytest.raises(ValueError, match="The Email field must be set"):
        django_user_model.objects.create_user(email=None, password="password123")


@pytest.mark.django_db
def test_create_superuser_without_is_staff_raises_error(django_user_model):
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        django_user_model.objects.create_superuser(email="admin@example.com", password="adminpass", is_staff=False)


@pytest.mark.django_db
def test_create_superuser_without_is_superuser_raises_error(django_user_model):
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        django_user_model.objects.create_superuser(email="admin@example.com", password="adminpass", is_superuser=False)
