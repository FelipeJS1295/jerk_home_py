from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import CustomUser, AFP, SaludEntidad, Cargo
from django.urls import reverse_lazy
from .forms import UserCreateForm
from mantenedores.models import Insumo, Proveedor, Cliente, Producto, ProductoInsumo
from django.db import transaction

class BaseConfigView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')

class ConfigHomeView(BaseConfigView, TemplateView):
    template_name = 'configuracion/config_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'home'
        return context

class ConfigUsuariosView(BaseConfigView, TemplateView):
    template_name = 'configuracion/config_usuarios.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'usuarios'
        return context

class ConfigMantenedoresView(BaseConfigView, TemplateView):
    template_name = 'configuracion/config_mantenedores.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['total_insumos'] = Insumo.objects.filter(active=True).count()
        context['total_proveedores'] = Proveedor.objects.filter(active=True).count()
        context['total_clientes'] = Cliente.objects.filter(active=True).count()
        context['total_productos'] = Producto.objects.filter(active=True).count()
        return context

class ConfigGeneralView(BaseConfigView, TemplateView):
    template_name = 'configuracion/config_general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'general'
        return context
    
class UserCreateView(BaseConfigView, CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = 'configuracion/user_form.html'
    success_url = reverse_lazy('configuracion:usuarios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'usuarios'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Usuario {form.instance.username} creado exitosamente')
        return response

# Vistas de Insumos
class InsumoListView(BaseConfigView, ListView):
    template_name = 'configuracion/mantenedores/insumo_list.html'
    model = Insumo
    context_object_name = 'insumos'

    def get_queryset(self):
        return Insumo.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        return context

class InsumoCreateView(BaseConfigView, CreateView):
    template_name = 'configuracion/mantenedores/insumo_form.html'
    model = Insumo
    fields = ['proveedor', 'codigo', 'nombre', 'unidad_medida', 'precio_costo', 'precio_venta']
    success_url = reverse_lazy('configuracion:insumos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['titulo'] = 'Crear Insumo'
        return context

class InsumoUpdateView(BaseConfigView, UpdateView):
    template_name = 'configuracion/mantenedores/insumo_form.html'
    model = Insumo
    fields = ['proveedor', 'codigo', 'nombre', 'unidad_medida', 'precio_costo', 'precio_venta']
    success_url = reverse_lazy('configuracion:insumos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['titulo'] = 'Editar Insumo'
        return context

class InsumoDeleteView(BaseConfigView, DeleteView):
    model = Insumo
    success_url = reverse_lazy('configuracion:insumos')

    def delete(self, request, *args, **kwargs):
        insumo = self.get_object()
        insumo.active = False
        insumo.save()
        messages.success(request, 'Insumo eliminado exitosamente')
        return redirect(self.success_url)

# Vistas de Proveedores
class ProveedorListView(BaseConfigView, ListView):
    template_name = 'configuracion/mantenedores/proveedor_list.html'
    model = Proveedor
    context_object_name = 'proveedores'

    def get_queryset(self):
        return Proveedor.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        return context

class ProveedorCreateView(BaseConfigView, CreateView):
    template_name = 'configuracion/mantenedores/proveedor_form.html'
    model = Proveedor
    fields = ['rut', 'nombre', 'contacto', 'email']
    success_url = reverse_lazy('configuracion:proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['titulo'] = 'Crear Proveedor'
        return context

class ProveedorUpdateView(BaseConfigView, UpdateView):
    template_name = 'configuracion/mantenedores/proveedor_form.html'
    model = Proveedor
    fields = ['rut', 'nombre', 'contacto', 'email']
    success_url = reverse_lazy('configuracion:proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['titulo'] = 'Editar Proveedor'
        return context

class ProveedorDeleteView(BaseConfigView, DeleteView):
    model = Proveedor
    success_url = reverse_lazy('configuracion:proveedores')

    def delete(self, request, *args, **kwargs):
        proveedor = self.get_object()
        proveedor.active = False
        proveedor.save()
        messages.success(request, 'Proveedor eliminado exitosamente')
        return redirect(self.success_url)

# Vistas de Clientes
class ClienteListView(BaseConfigView, ListView):
    template_name = 'configuracion/mantenedores/cliente_list.html'
    model = Cliente
    context_object_name = 'clientes'

    def get_queryset(self):
        return Cliente.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        return context

class ClienteCreateView(BaseConfigView, CreateView):
    template_name = 'configuracion/mantenedores/cliente_form.html'
    model = Cliente
    fields = ['rut', 'nombre', 'contacto', 'email']
    success_url = reverse_lazy('configuracion:clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['titulo'] = 'Crear Cliente'
        return context

class ClienteUpdateView(BaseConfigView, UpdateView):
    template_name = 'configuracion/mantenedores/cliente_form.html'
    model = Cliente
    fields = ['rut', 'nombre', 'contacto', 'email']
    success_url = reverse_lazy('configuracion:clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['titulo'] = 'Editar Cliente'
        return context

class ClienteDeleteView(BaseConfigView, DeleteView):
    model = Cliente
    success_url = reverse_lazy('configuracion:clientes')

    def delete(self, request, *args, **kwargs):
        cliente = self.get_object()
        cliente.active = False
        cliente.save()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect(self.success_url)

# Vistas de Productos
class BaseProductoView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')

class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'configuracion/mantenedores/producto_list.html'
    context_object_name = 'productos'

    def get_queryset(self):
        return Producto.objects.filter(active=True).prefetch_related(
            'productoinsumo_set',
            'productoinsumo_set__insumo',
            'productoinsumo_set__insumo__unidad_medida'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        return context

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    template_name = 'configuracion/mantenedores/producto_form.html'
    fields = ['sku', 'nombre', 'nombre_esqueleto', 'nombre_armado_esqueleto',
              'nombre_corte_esqueleto', 'costo_costura', 'costo_tapiceria',
              'costo_corte', 'costo_armado', 'costo_corte_armado', 'precio_venta_promedio']
    success_url = reverse_lazy('configuracion:productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['insumos'] = Insumo.objects.filter(active=True)
        context['titulo'] = 'Crear Producto'
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Guardar el producto
                self.object = form.save()
                
                # Obtener los insumos seleccionados
                insumos_seleccionados = self.request.POST.getlist('insumo_selected[]')
                print("Insumos seleccionados:", insumos_seleccionados)  # Debug

                # Crear las relaciones con los insumos
                for insumo_id in insumos_seleccionados:
                    cantidad = self.request.POST.get(f'cantidad_{insumo_id}')
                    print(f"Procesando insumo {insumo_id} con cantidad {cantidad}")  # Debug
                    
                    if cantidad:
                        try:
                            cantidad = float(cantidad)
                            ProductoInsumo.objects.create(
                                producto=self.object,
                                insumo_id=insumo_id,
                                cantidad=cantidad
                            )
                            print(f"Insumo {insumo_id} agregado con éxito")  # Debug
                        except ValueError:
                            print(f"Error al convertir cantidad para insumo {insumo_id}")  # Debug
                
                messages.success(self.request, 'Producto creado exitosamente')
                return redirect(self.success_url)
                
        except Exception as e:
            print(f"Error al guardar: {str(e)}")  # Debug
            messages.error(self.request, f'Error al guardar el producto: {str(e)}')
            return self.form_invalid(form)

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = 'configuracion/mantenedores/producto_form.html'
    fields = ['sku', 'nombre', 'nombre_esqueleto', 'nombre_armado_esqueleto',
              'nombre_corte_esqueleto', 'costo_costura', 'costo_tapiceria',
              'costo_corte', 'costo_armado', 'costo_corte_armado', 'precio_venta_promedio']
    success_url = reverse_lazy('configuracion:productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['insumos'] = Insumo.objects.filter(active=True)
        context['titulo'] = 'Editar Producto'
        # Marcar los insumos que ya están asociados
        producto_insumos = self.object.productoinsumo_set.all()
        context['producto_insumos'] = {pi.insumo_id: pi.cantidad for pi in producto_insumos}
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save()
                
                # Eliminar relaciones anteriores
                self.object.productoinsumo_set.all().delete()
                
                # Obtener los insumos seleccionados
                insumos_seleccionados = self.request.POST.getlist('insumo_selected[]')
                
                # Crear las nuevas relaciones
                for insumo_id in insumos_seleccionados:
                    cantidad = self.request.POST.get(f'cantidad_{insumo_id}')
                    if cantidad:
                        try:
                            cantidad = float(cantidad)
                            ProductoInsumo.objects.create(
                                producto=self.object,
                                insumo_id=insumo_id,
                                cantidad=cantidad
                            )
                        except ValueError:
                            continue
                
                messages.success(self.request, 'Producto actualizado exitosamente')
                return redirect(self.success_url)
                
        except Exception as e:
            messages.error(self.request, f'Error al actualizar el producto: {str(e)}')
            return self.form_invalid(form)

class ProductoDeleteView(BaseProductoView, DeleteView):
    model = Producto
    success_url = reverse_lazy('configuracion:productos')

    def delete(self, request, *args, **kwargs):
        producto = self.get_object()
        producto.active = False
        producto.save()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect(self.success_url)

