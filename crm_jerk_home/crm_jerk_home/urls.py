from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import (
    CustomLoginView, 
    CustomLogoutView, 
    RegistroView, 
    HomeView, ConfigHomeView, ConfigUsuariosView, 
    ConfigMantenedoresView, ConfigGeneralView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('configuracion/', include('configuracion.urls')),
    
    
    path('configuracion/', ConfigHomeView.as_view(), name='config_home'),
    path('configuracion/usuarios/', ConfigUsuariosView.as_view(), name='config_usuarios'),
    path('configuracion/mantenedores/', ConfigMantenedoresView.as_view(), name='config_mantenedores'),
    path('configuracion/general/', ConfigGeneralView.as_view(), name='config_general'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)