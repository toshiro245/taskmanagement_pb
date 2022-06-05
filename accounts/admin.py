from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'is_staff']
    ordering = ('email',)

    fieldsets = (
        ('UserInfo', {'fields':('email', 'password', 'country', 'create_at', 'update_at')}),
        ('Permission', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )

    add_fieldsets = (
        ('UserInfo', {
            'fields':('email', 'password', 'confirm_password', 'country')
        }),
    )


admin.site.register(User, CustomizeUserAdmin)