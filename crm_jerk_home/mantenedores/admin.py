from django.contrib import admin
from .models import (
    Proveedor,
    Cliente,
    UnidadMedida,
    Insumo,
    Producto,
    ProductoInsumo
)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'contacto', 'email', 'active')
    search_fields = ('rut', 'nombre', 'email')
    list_filter = ('active',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'contacto', 'email', 'active')
    search_fields = ('rut', 'nombre', 'email')
    list_filter = ('active',)

@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo', 'active')
    search_fields = ('nombre', 'simbolo')

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'proveedor', 'unidad_medida', 
                   'precio_costo', 'precio_venta', 'active')
    search_fields = ('codigo', 'nombre')
    list_filter = ('proveedor', 'unidad_medida', 'active')

class ProductoInsumoInline(admin.TabularInline):
    model = ProductoInsumo
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'precio_venta_promedio', 'active')
    search_fields = ('sku', 'nombre')
    list_filter = ('active',)
    inlines = [ProductoInsumoInline]