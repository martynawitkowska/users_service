from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer, CustomUser, Department, Organization, Tenant


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	# Configure the fields to display in the admin
	list_display = ('email', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_active')
	search_fields = ('email',)
	ordering = ('email',)

	# Customizations for edit forms in the admin
	fieldsets = (
		(None, {'fields': ('email', 'password', 'tenant')}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(
			None,
			{
				'classes': ('wide',),
				'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions'),
			},
		),
	)


admin.site.register(Organization)
admin.site.register(Tenant)
admin.site.register(Customer)
admin.site.register(Department)
