import re


def normalizar_numero_guia(numero: str) -> str:
    if not numero:
        return ''
    numero = numero.strip().upper()
    numero = re.sub(r'[\s\-_]+', '', numero)
    return numero
