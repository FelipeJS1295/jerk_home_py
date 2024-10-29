from django.core.management.base import BaseCommand
from users.models import AFP, SaludEntidad, Cargo

class Command(BaseCommand):
    help = 'Carga los datos iniciales necesarios para el sistema'

    def handle(self, *args, **kwargs):
        # Crear AFPs
        afps_data = [
            {'nombre': 'Capital', 'codigo': 'CAP'},
            {'nombre': 'Cuprum', 'codigo': 'CUP'},
            {'nombre': 'Habitat', 'codigo': 'HAB'},
            {'nombre': 'PlanVital', 'codigo': 'PVT'},
            {'nombre': 'ProVida', 'codigo': 'PRV'},
            {'nombre': 'Modelo', 'codigo': 'MOD'},
            {'nombre': 'Uno', 'codigo': 'UNO'},
        ]
        
        for afp_data in afps_data:
            AFP.objects.get_or_create(**afp_data)
            
        self.stdout.write(self.style.SUCCESS('AFPs creadas exitosamente'))

        # Crear Entidades de Salud
        salud_data = [
            {'nombre': 'Fonasa', 'codigo': 'FON'},
            {'nombre': 'Banmédica', 'codigo': 'BAN'},
            {'nombre': 'Colmena', 'codigo': 'COL'},
            {'nombre': 'Cruz Blanca', 'codigo': 'CRB'},
            {'nombre': 'Nueva Masvida', 'codigo': 'NMV'},
            {'nombre': 'Consalud', 'codigo': 'CON'},
            {'nombre': 'Vida Tres', 'codigo': 'VDT'},
        ]
        
        for salud in salud_data:
            SaludEntidad.objects.get_or_create(**salud)
            
        self.stdout.write(self.style.SUCCESS('Entidades de Salud creadas exitosamente'))

        # Crear Cargos básicos
        cargos_data = [
            {'nombre': 'Administrador', 'descripcion': 'Administrador del sistema'},
            {'nombre': 'Ventas', 'descripcion': 'Vendedor de muebles'},
            {'nombre': 'Tapiceria', 'descripcion': 'Fabricante de muebles'},
            {'nombre': 'Costura', 'descripcion': 'Costura de muebles'},
            {'nombre': 'Bodega', 'descripcion': 'Encargado de bodega'},
            {'nombre': 'Cojineria', 'descripcion': 'Cojinero'},
            {'nombre': 'Embalaje', 'descripcion': 'Embalaje'},
            {'nombre': 'Finanzas', 'descripcion': 'Finanzas'},
            {'nombre': 'RRHH', 'descripcion': 'Recursos Humanos'},
            {'nombre': 'Despacho', 'descripcion': 'Despacho'},
        ]
        
        for cargo in cargos_data:
            Cargo.objects.get_or_create(**cargo)
            
        self.stdout.write(self.style.SUCCESS('Cargos creados exitosamente'))