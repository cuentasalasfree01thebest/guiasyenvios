from django import forms
from .models import Guia
from .utils import normalizar_numero_guia

INPUT_ATTRS = {
    'class': 'form-control',
}


class GuiaForm(forms.ModelForm):
    class Meta:
        model = Guia
        fields = [
            'numero',
            'empresa',
            'valor',
            'remitente_nombre',
            'remitente_tel',
            'remitente_ciudad',
            'remitente_depto',
            'remitente_dir',
            'dest_nombre',
            'dest_tel',
            'dest_ciudad',
            'dest_depto',
            'dest_dir',
            'dest_peso',
            'dest_obs',
        ]
        labels = {
            'numero': 'Número de guía',
            'empresa': 'Empresa',
            'valor': 'Valor a cobrar',
            'remitente_nombre': 'Nombre completo',
            'remitente_tel': 'Teléfono',
            'remitente_ciudad': 'Ciudad',
            'remitente_depto': 'Departamento',
            'remitente_dir': 'Dirección',
            'dest_nombre': 'Nombre completo',
            'dest_tel': 'Teléfono',
            'dest_ciudad': 'Ciudad',
            'dest_depto': 'Departamento',
            'dest_dir': 'Dirección',
            'dest_peso': 'Peso',
            'dest_obs': 'Observaciones',
        }
        widgets = {
            'numero': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Ej: 750006906073'}),
            'empresa': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Tu Empresa S.A.S'}),
            'valor': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': '$50,000'}),
            'remitente_nombre': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Juan Pérez'}),
            'remitente_tel': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': '3001234567'}),
            'remitente_ciudad': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Medellín'}),
            'remitente_depto': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Antioquia'}),
            'remitente_dir': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Cra 50 #45-10'}),
            'dest_nombre': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'María García'}),
            'dest_tel': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': '3109876543'}),
            'dest_ciudad': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Bogotá'}),
            'dest_depto': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Cundinamarca'}),
            'dest_dir': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Cll 100 #15-20'}),
            'dest_peso': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': '1.5 kg'}),
            'dest_obs': forms.TextInput(attrs={**INPUT_ATTRS, 'placeholder': 'Frágil, no voltear...'}),
        }

    def clean_numero(self):
        numero = normalizar_numero_guia(self.cleaned_data.get('numero', ''))
        if not numero:
            raise forms.ValidationError('El número de guía es obligatorio.')
        if Guia.objects.filter(numero=numero).exists():
            raise forms.ValidationError(f'Ya existe una guía con el número #{numero}.')
        return numero
