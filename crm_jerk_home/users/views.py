# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import CustomUser, AFP, SaludEntidad, Cargo
from django.db.models import Count

class HomeView(LoginRequiredMixin, TemplateView):
    """Vista para la página principal"""
    template_name = 'home.html'
    login_url = 'login'

class CustomLoginView(LoginView):
    """Vista personalizada para el login"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña inválidos. Por favor intente nuevamente.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    """Vista personalizada para el logout"""
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return super().dispatch(request, *args, **kwargs)

class RegistroView(CreateView):
    """Vista para el registro de usuarios"""
    form_class = CustomUserCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registro exitoso. Por favor inicia sesión.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Error en el registro. Por favor revisa los datos ingresados.')
        return super().form_invalid(form)
    
class ConfigBaseView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')

class ConfigHomeView(ConfigBaseView, TemplateView):
    template_name = 'configuracion/config_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'home'
        context['usuarios_activos'] = CustomUser.objects.filter(is_active=True).count()
        context['total_departamentos'] = Cargo.objects.count()
        return context

class ConfigUsuariosView(ConfigBaseView, TemplateView):
    template_name = 'configuracion/config_usuarios.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'usuarios'
        context['users'] = CustomUser.objects.all().select_related('cargo')
        return context

class ConfigMantenedoresView(ConfigBaseView, TemplateView):
    template_name = 'configuracion/config_mantenedores.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mantenedores'
        context['afps'] = AFP.objects.all()
        context['entidades_salud'] = SaludEntidad.objects.all()
        context['cargos'] = Cargo.objects.all()
        return context

class ConfigGeneralView(ConfigBaseView, TemplateView):
    template_name = 'configuracion/config_general.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'general'
        # Aquí puedes agregar la configuración general de tu sistema
        context['config'] = {
            'company_name': 'Jerk Home',
            'company_rut': '',
            'company_address': '',
            'timezone': 'America/Santiago',
            'enable_notifications': True,
        }
        return context