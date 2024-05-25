from django import template

register = template.Library()

@register.filter
def first_key_value(dictionary):
    if isinstance(dictionary, dict) and dictionary:
        first_key = next(iter(dictionary))
        return (first_key, dictionary[first_key])
    return (None, None)
