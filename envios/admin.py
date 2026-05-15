from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Guia

@admin.register(Guia)
class GuiaAdmin(admin.ModelAdmin):
    list_display = [
        'numero',
        'remitente_nombre',
        'dest_nombre',
        'dest_ciudad',
        'paso_actual',
        'boton_rastreo',
        'boton_pdf',
        'fecha_creacion',
    ]
    list_editable = ['paso_actual']
    search_fields = ['numero', 'remitente_nombre', 'dest_nombre', 'dest_ciudad']
    list_filter = ['paso_actual', 'dest_ciudad', 'empresa']
    readonly_fields = ['fecha_creacion', 'fecha_actualizado']

    def boton_rastreo(self, obj):
        url = reverse('rastrear', args=[obj.numero])
        return format_html(
            '<a href="{}" target="_blank" '
            'style="background:#2563eb;color:#fff;padding:6px 10px;border-radius:6px;text-decoration:none;font-size:12px;font-weight:600;">'
            'Rastreo</a>',
            url
        )
    boton_rastreo.short_description = 'Portal'

    def boton_pdf(self, obj):
        url = reverse('guia_vista', args=[obj.numero])
        return format_html(
            '<a href="{}" target="_blank" '
            'style="background:#111827;color:#fff;padding:6px 10px;border-radius:6px;text-decoration:none;font-size:12px;font-weight:600;">'
            'PDF</a>',
            url
        )
    boton_pdf.short_description = 'Guía PDF'


original_index = admin.site.index

def custom_index(request, extra_context=None):
    from .models import Guia

    extra_context = extra_context or {}
    extra_context.update({
        'total_guias': Guia.objects.count(),
        'pendientes': Guia.objects.filter(paso_actual=0).count(),
        'transito': Guia.objects.filter(paso_actual__gte=1, paso_actual__lt=5).count(),
        'entregadas': Guia.objects.filter(paso_actual=5).count(),
        'ultimas_guias': Guia.objects.order_by('-fecha_creacion')[:5],
    })
    return original_index(request, extra_context=extra_context)

admin.site.index = custom_index
admin.site.site_header = "Panel de Envíos"
admin.site.site_title = "Admin Envíos"
admin.site.index_title = "Dashboard"