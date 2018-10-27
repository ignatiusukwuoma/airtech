from django import template

register = template.Library()


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return '{}hr {}m'.format(hours, minutes)


@register.filter
def add_time(td, ta):
    return td + ta
