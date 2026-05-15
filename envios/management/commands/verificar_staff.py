from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Verifica que los superusuarios tengan is_staff activo para acceder al admin'

    def handle(self, *args, **options):
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)

        if not superusers.exists():
            self.stdout.write(self.style.WARNING('No hay superusuarios. Crea uno con: python manage.py createsuperuser'))
            return

        for user in superusers:
            if user.is_staff:
                self.stdout.write(self.style.SUCCESS(f'OK: {user.username} (is_staff activo)'))
            else:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
                self.stdout.write(self.style.WARNING(f'Corregido: {user.username} — se activó is_staff'))
