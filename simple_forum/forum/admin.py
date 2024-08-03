from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and obj.username == 'moder':
            group, created = Group.objects.get_or_create(name='Moderators')
            if created:
                permissions = Permission.objects.filter(
                    content_type__model__in=['topic', 'reply']
                )
                group.permissions.set(permissions)
            obj.groups.add(group)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
