from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from datetime import datetime

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        options.setdefault('interactive', True)
        username = options.get('username')
        email = options.get('email')
        database = options.get('database')

        if not username:
            username = self.get_input_data(self.username_field, 'Username')
        if not email:
            email = self.get_input_data('email', 'Email')

        # Campos adicionales requeridos
        rut = input('RUT (ejemplo: 12345678-9): ')
        fecha_nacimiento = input('Fecha de nacimiento (YYYY-MM-DD): ')
        direccion = input('Dirección: ')
        telefono = input('Teléfono (+569XXXXXXXX): ')

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        except ValueError:
            raise CommandError('Formato de fecha incorrecto. Use YYYY-MM-DD')

        user_data = {
            'username': username,
            'email': email,
            'rut': rut,
            'fecha_nacimiento': fecha_nacimiento,
            'direccion': direccion,
            'telefono': telefono,
            'is_staff': True,
            'is_superuser': True,
            'afp_id': 1,  # Asignaremos valores por defecto para AFPy Salud
            'salud_id': 1,
            'cargo_id': 1,
            'tipo_sueldo': 'FIJO'
        }

        user_data['password'] = None
        self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

        if options.get('verbosity', 0) >= 1:
            self.stdout.write("Superusuario creado exitosamente.")