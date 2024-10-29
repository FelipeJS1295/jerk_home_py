from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica dos números, maneja decimales correctamente"""
    try:
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        return value * arg
    except (ValueError, TypeError, InvalidOperation):
        return 0

@register.filter
def format_money(value):
    """Formatea un número como moneda chilena"""
    try:
        value = Decimal(str(value))
        return f"${value:,.0f}".replace(',', '.')
    except (ValueError, TypeError, InvalidOperation):
        return "$0"