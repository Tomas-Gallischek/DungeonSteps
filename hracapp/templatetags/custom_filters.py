from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Nahradí v `value` první část argumentu `arg` druhou částí.
    Argument `arg` musí být ve formátu "co_se_nahrazuje:cim_se_nahrazuje".
    Příklad: {{ "text_s_podtrzitkem"|replace:"_:-" }}
    """
    try:
        old, new = arg.split(':')
        return value.replace(old, new)
    except ValueError:
        return value