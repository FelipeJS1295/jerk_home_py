# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'rut', 
                'fecha_nacimiento', 'direccion', 'telefono', 'afp', 'salud', 'tipo_sueldo')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels en español
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo electrónico'
        
        # Hacer algunos campos obligatorios
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        
        # Personalizar mensajes de ayuda
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, números y @/./+/-/_ solamente.'
        self.fields['password1'].help_text = 'Tu contraseña debe contener al menos 8 caracteres.'
        self.fields['rut'].help_text = 'Formato: 12345678-9'
        self.fields['fecha_nacimiento'].help_text = 'Formato: YYYY-MM-DD'