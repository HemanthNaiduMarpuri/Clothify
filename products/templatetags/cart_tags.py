from django import template
register = template.Library()

@register.filter
def mul(qty, price):
    try:
        return qty * price
    except:
        return 0
