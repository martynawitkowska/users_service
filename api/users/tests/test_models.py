import pytest
from django.db.utils import IntegrityError

from users.models import Tenant
from users.models.user import CustomUserManager


@pytest.mark.django_db
def test_custom_user_creation(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    user = django_user_model.objects.create_user(
        email="testuser@example.com", password="securepassword", tenant=tenant
    )
    assert user.email == "testuser@example.com"
    assert user.check_password("securepassword")
    assert user.tenant == tenant


@pytest.mark.django_db
def test_custom_user_creation_without_email(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    with pytest.raises(ValueError):
        django_user_model.objects.create_user(email=None, password="securepassword", tenant=tenant)


@pytest.mark.django_db
def test_custom_user_unique_email_constraint(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    django_user_model.objects.create_user(email="testuser@example.com", password="securepassword", tenant=tenant)

    with pytest.raises(IntegrityError):
        django_user_model.objects.create_user(email="testuser@example.com", password="anotherpassword", tenant=tenant)


@pytest.mark.django_db
def test_custom_user_manager_superuser_creation(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    superuser = django_user_model.objects.create_superuser(
        email="admin@example.com", password="adminpassword", tenant=tenant
    )
    assert superuser.email == "admin@example.com"
    assert superuser.is_superuser
    assert superuser.is_staff


@pytest.mark.django_db
def test_custom_user_str_representation(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    user = django_user_model.objects.create_user(
        email="testuser@example.com", password="securepassword", tenant=tenant
    )
    assert str(user) == "testuser@example.com"


@pytest.mark.django_db
def test_create_user(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    user = django_user_model.objects.create_user(
        email="user@example.com", password="securepassword", tenant=tenant
    )
    assert user.email == "user@example.com"
    assert user.check_password("securepassword")
    assert user.tenant == tenant
    assert user.is_active is True



@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    tenant = Tenant.objects.create(name="Test Tenant")
    manager = CustomUserManager()
    with pytest.raises(ValueError, match="The Email field must be set"):
        manager.create_user(email=None, password="password", tenant=tenant)


@pytest.mark.django_db
def test_create_user(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    user = django_user_model.objects.create_user(
        email="user@example.com", password="securepassword", tenant=tenant
    )
    assert user.email == "user@example.com"
    assert user.check_password("securepassword")
    assert user.tenant == tenant
    assert user.is_active is True


@pytest.mark.django_db
def test_create_user_without_email_raises_error(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    with pytest.raises(ValueError, match="The Email field must be set"):
        django_user_model.objects.create_user(
            email=None, password="password", tenant=tenant
        )


@pytest.mark.django_db
def test_create_superuser(django_user_model):
    tenant = Tenant.objects.create(name="Test Tenant")
    superuser = django_user_model.objects.create_superuser(
        email="admin@example.com", password="securepassword", tenant=tenant
    )
    assert superuser.email == "admin@example.com"
    assert superuser.check_password("securepassword")
    assert superuser.tenant == tenant
    assert superuser.is_staff is True
    assert superuser.is_superuser is True



@pytest.mark.django_db
def test_create_superuser_without_is_staff_raises_error():
    tenant = Tenant.objects.create(name="Test Tenant")
    manager = CustomUserManager()
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        manager.create_superuser(email="admin@example.com", password="securepassword", tenant=tenant, is_staff=False)


@pytest.mark.django_db
def test_create_superuser_without_is_superuser_raises_error():
    tenant = Tenant.objects.create(name="Test Tenant")
    manager = CustomUserManager()
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        manager.create_superuser(email="admin@example.com", password="securepassword", tenant=tenant,
                                 is_superuser=False)
