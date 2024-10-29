from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Proveedor(BaseModel):
    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dkK]$',
        message='Ingrese un RUT válido. Ejemplo: 12345678-9'
    )
    
    rut = models.CharField(
        max_length=12,
        validators=[rut_validator],
        unique=True,
        verbose_name='RUT'
    )
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

class Cliente(BaseModel):
    rut_validator = RegexValidator(
        regex=r'^\d{7,8}-[\dkK]$',
        message='Ingrese un RUT válido. Ejemplo: 12345678-9'
    )
    
    rut = models.CharField(
        max_length=12,
        validators=[rut_validator],
        unique=True,
        verbose_name='RUT'
    )
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class UnidadMedida(BaseModel):
    nombre = models.CharField(max_length=50, unique=True)
    simbolo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} ({self.simbolo})"

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

class Insumo(BaseModel):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    
    

    def clean(self):
        if self.precio_venta < self.precio_costo:
            raise ValidationError('El precio de venta no puede ser menor al precio de costo')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'

class Producto(BaseModel):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    nombre_esqueleto = models.CharField(max_length=200)
    nombre_armado_esqueleto = models.CharField(max_length=200)
    nombre_corte_esqueleto = models.CharField(max_length=200)
    
    # Costos de producción
    costo_costura = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    costo_tapiceria = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    costo_corte = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    costo_armado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    costo_corte_armado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    precio_venta_promedio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    insumos = models.ManyToManyField(
        Insumo,
        through='ProductoInsumo',
        related_name='productos'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

    def get_costo_total(self):
        costo_insumos = sum(
            pi.cantidad * pi.insumo.precio_costo 
            for pi in self.productoinsumo_set.all()
        )
        costo_produccion = (
            self.costo_costura + 
            self.costo_tapiceria + 
            self.costo_corte + 
            self.costo_armado + 
            self.costo_corte_armado
        )
        return costo_insumos + costo_produccion

    def get_margen(self):
        costo_total = self.get_costo_total()
        if self.precio_venta_promedio and self.precio_venta_promedio > 0:
            margen = ((self.precio_venta_promedio - costo_total) / self.precio_venta_promedio) * 100
            return round(margen, 1)
        return 0

class ProductoInsumo(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    class Meta:
        verbose_name = 'Insumo de Producto'
        verbose_name_plural = 'Insumos de Productos'
        unique_together = ['producto', 'insumo']

    def __str__(self):
        return f"{self.producto.nombre} - {self.insumo.nombre} ({self.cantidad})"

    @property
    def subtotal(self):
        """Calcula el subtotal (cantidad * precio_costo)"""
        return self.cantidad * self.insumo.precio_costo