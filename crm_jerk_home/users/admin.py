from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AFP, SaludEntidad, Cargo

@admin.register(AFP)
class AFPAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo')
    search_fields = ('nombre', 'codigo')

@admin.register(SaludEntidad)
class SaludEntidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo')
    search_fields = ('nombre', 'codigo')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('rut', 'first_name', 'last_name', 'email', 'cargo', 'is_active')
    list_filter = ('is_active', 'cargo', 'tipo_sueldo', 'afp', 'salud')
    search_fields = ('rut', 'first_name', 'last_name', 'email')
    ordering = ('first_name',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'username', 'password', 'first_name', 'last_name', 'email',
                'rut', 'fecha_nacimiento', 'direccion', 'telefono'
            )
        }),
        ('Información Laboral', {
            'fields': (
                'cargo', 'afp', 'salud', 'tipo_sueldo', 'fecha_ingreso'
            )
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'last_name',
                'email', 'rut', 'fecha_nacimiento', 'direccion', 'telefono',
                'cargo', 'afp', 'salud', 'tipo_sueldo', 'fecha_ingreso',
                'is_active', 'is_staff'
            ),
        }),
    )