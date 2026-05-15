from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Guia
from .forms import GuiaForm
from .utils import normalizar_numero_guia

PASOS_INFO = [
    {'idx': 0, 'nombre': 'Envío recogido',              'icono': '📦', 'desc': 'El paquete fue recogido en origen'},
    {'idx': 1, 'nombre': 'En Centro Logístico Origen',  'icono': '🏭', 'desc': 'Llegó al centro logístico de origen'},
    {'idx': 2, 'nombre': 'Viajando a tu destino',       'icono': '🚚', 'desc': 'El paquete está en tránsito'},
    {'idx': 3, 'nombre': 'En Centro Logístico Destino', 'icono': '🏬', 'desc': 'Llegó al centro logístico más cercano'},
    {'idx': 4, 'nombre': 'En camino hacia ti',          'icono': '🛵', 'desc': 'El mensajero está en camino'},
    {'idx': 5, 'nombre': 'Entregado exitosamente',      'icono': '✅', 'desc': 'Tu paquete fue entregado'},
]


def inicio(request):
    return redirect('rastrear_inicio')


@staff_member_required
def crear_guia(request):
    if request.method == 'POST':
        form = GuiaForm(request.POST)
        if form.is_valid():
            guia = form.save()
            messages.success(request, f'✅ Guía #{guia.numero} creada exitosamente.')
            return redirect('rastrear', numero=guia.numero)
    else:
        form = GuiaForm()
    return render(request, 'envios/crear_guia.html', {'form': form})


def rastrear(request, numero=None):
    guia = None
    pasos_estado = []
    if numero:
        numero_norm = normalizar_numero_guia(numero)
        if numero_norm and numero_norm != numero:
            return redirect('rastrear', numero=numero_norm)
        numero = numero_norm
        guia = Guia.objects.filter(numero=numero).first()
        if guia:
            for paso in PASOS_INFO:
                i = paso['idx']
                if i < guia.paso_actual or guia.paso_actual == 5:
                    estado = 'completado'
                elif i == guia.paso_actual:
                    estado = 'activo'
                else:
                    estado = 'pendiente'
                pasos_estado.append({**paso, 'estado': estado})
    return render(request, 'envios/rastrear.html', {
        'guia': guia,
        'pasos': pasos_estado,
        'numero_buscado': numero,
    })


def buscar_guia(request):
    numero = normalizar_numero_guia(request.GET.get('numero', ''))
    if numero:
        return redirect('rastrear', numero=numero)
    messages.warning(request, 'Ingresa un número de guía para rastrear.')
    return redirect('rastrear_inicio')


@staff_member_required
def guia_vista(request, numero):
    numero = normalizar_numero_guia(numero)
    guia = get_object_or_404(Guia, numero=numero)
    return render(request, 'envios/guia_pdf.html', {
        'guia': guia,
        'modo_pdf': False,
    })


@staff_member_required
def guia_pdf(request, numero):
    numero = normalizar_numero_guia(numero)
    guia = get_object_or_404(Guia, numero=numero)
    return render(request, 'envios/guia_pdf.html', {
        'guia': guia,
        'modo_pdf': True,
    })
