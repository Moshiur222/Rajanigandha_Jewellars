from django import template

register = template.Library()


@register.filter
def bd_currency(value):
    try:
        value = float(value)

        integer, decimal = f"{value:.2f}".split(".")

        integer = str(integer)

        if len(integer) <= 3:
            result = integer
        else:
            last3 = integer[-3:]
            rest = integer[:-3]

            parts = []

            while len(rest) > 2:
                parts.insert(0, rest[-2:])
                rest = rest[:-2]

            if rest:
                parts.insert(0, rest)

            result = ",".join(parts) + "," + last3

        return f"{result}.{decimal}"

    except:
        return value
    

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