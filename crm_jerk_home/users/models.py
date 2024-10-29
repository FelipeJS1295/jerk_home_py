from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class AFP(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'AFP'
        verbose_name_plural = 'AFPs'

    def __str__(self):
        return self.nombre

class SaludEntidad(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Entidad de Salud'
        verbose_name_plural = 'Entidades de Salud'

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    TIPO_SUELDO_CHOICES = [
        ('FIJO', 'Sueldo Fijo'),
        ('PARCIAL', 'Sueldo Parcial'),
    ]

    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dkK]$',
        message='Ingrese un RUT válido. Ejemplo: 12345678-9'
    )
    phone_validator = RegexValidator(
        regex=r'^\+?56?\d{9}$',
        message='Ingrese un número válido. Ejemplo: +56912345678'
    )

    rut = models.CharField(
        max_length=12,
        validators=[rut_validator],
        unique=True,
        verbose_name='RUT'
    )
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento',
        null=True,  # Permitimos null temporalmente
        blank=True  # Permitimos blank temporalmente
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name='Dirección',
        null=True,
        blank=True
    )
    telefono = models.CharField(
        max_length=12,
        validators=[phone_validator],
        verbose_name='Teléfono',
        null=True,
        blank=True
    )
    
    afp = models.ForeignKey(
        AFP,
        on_delete=models.PROTECT,
        verbose_name='AFP',
        null=True,
        blank=True
    )
    salud = models.ForeignKey(
        SaludEntidad,
        on_delete=models.PROTECT,
        verbose_name='Entidad de Salud',
        null=True,
        blank=True
    )
    cargo = models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        verbose_name='Cargo',
        null=True,
        blank=True
    )
    tipo_sueldo = models.CharField(
        max_length=10,
        choices=TIPO_SUELDO_CHOICES,
        default='FIJO',
        verbose_name='Tipo de Sueldo'
    )
    fecha_ingreso = models.DateField(
        verbose_name='Fecha de Ingreso',
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rut}"