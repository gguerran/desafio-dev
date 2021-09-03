from django import template

register = template.Library()


@register.simple_tag(name="mask_cpf")
def mask_cpf(cpf):
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
