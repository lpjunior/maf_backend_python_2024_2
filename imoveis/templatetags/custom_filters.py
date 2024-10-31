from django import template

register = template.Library()

@register.filter
def pago_sim_nao(value):
    return "Sim" if value else "Não"

@register.filter
def alertformat(value):
    return "danger" if value == 'error' else value