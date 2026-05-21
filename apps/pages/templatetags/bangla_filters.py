from django import template

register = template.Library()

EN_TO_BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")

@register.filter
def bn_number(value):
    if value is None:
        return ""
    return str(value).translate(EN_TO_BN)


@register.filter
def bn_price(value):
    if value is None:
        return "০"

    try:
        value = float(value)
        value = round(value, 2)

        if value.is_integer():
            value = int(value)

    except:
        pass

    return str(value).translate(EN_TO_BN)