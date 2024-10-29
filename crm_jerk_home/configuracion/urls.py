from django.urls import path
from .views import (
    ConfigHomeView,
    ConfigUsuariosView,
    ConfigMantenedoresView,
    ConfigGeneralView,
    UserCreateView, InsumoListView, InsumoCreateView, InsumoUpdateView, InsumoDeleteView,
    ProveedorListView, ProveedorCreateView, ProveedorUpdateView, ProveedorDeleteView,
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView,
)

app_name = 'configuracion'

urlpatterns = [
    path('', ConfigHomeView.as_view(), name='home'),
    path('usuarios/', ConfigUsuariosView.as_view(), name='usuarios'),
    path('usuarios/crear/', UserCreateView.as_view(), name='user_create'),
    path('mantenedores/', ConfigMantenedoresView.as_view(), name='mantenedores'),
    path('general/', ConfigGeneralView.as_view(), name='general'),
    
    # Insumos
    path('mantenedores/insumos/', InsumoListView.as_view(), name='insumos'),
    path('mantenedores/insumos/crear/', InsumoCreateView.as_view(), name='insumo_create'),
    path('mantenedores/insumos/<int:pk>/', InsumoUpdateView.as_view(), name='insumo_update'),
    path('mantenedores/insumos/<int:pk>/eliminar/', InsumoDeleteView.as_view(), name='insumo_delete'),
    
    # Proveedores
    path('mantenedores/proveedores/', ProveedorListView.as_view(), name='proveedores'),
    path('mantenedores/proveedores/crear/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('mantenedores/proveedores/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('mantenedores/proveedores/<int:pk>/eliminar/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
    
    # Clientes
    path('mantenedores/clientes/', ClienteListView.as_view(), name='clientes'),
    path('mantenedores/clientes/crear/', ClienteCreateView.as_view(), name='cliente_create'),
    path('mantenedores/clientes/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('mantenedores/clientes/<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # Productos
    path('mantenedores/productos/', ProductoListView.as_view(), name='productos'),
    path('mantenedores/productos/crear/', ProductoCreateView.as_view(), name='producto_create'),
    path('mantenedores/productos/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('mantenedores/productos/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='producto_delete'),
]