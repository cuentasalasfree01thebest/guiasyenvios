from django.core.management.base import BaseCommand
from envios.models import Guia
from envios.utils import normalizar_numero_guia


class Command(BaseCommand):
    help = 'Normaliza números de guía existentes en la base de datos'

    def handle(self, *args, **options):
        actualizadas = 0
        for guia in Guia.objects.all():
            norm = normalizar_numero_guia(guia.numero)
            if norm and norm != guia.numero:
                if Guia.objects.filter(numero=norm).exclude(pk=guia.pk).exists():
                    self.stdout.write(self.style.ERROR(
                        f'Conflicto: #{guia.numero} → #{norm} ya existe en otra guía'
                    ))
                    continue
                guia.numero = norm
                guia.save(update_fields=['numero'])
                actualizadas += 1
                self.stdout.write(f'Actualizada: {norm}')

        self.stdout.write(self.style.SUCCESS(f'Listo. {actualizadas} guía(s) normalizada(s).'))
