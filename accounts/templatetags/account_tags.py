from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def days_on_site(date_joined):
    delta = timezone.now() - date_joined
    days = delta.days

    if days <= 0:
        return "перший день"

    last_two = days % 100
    last_digit = days % 10

    if 11 <= last_two <= 14:
        word = "днів"
    elif last_digit == 1:
        word = "день"
    elif 2 <= last_digit <= 4:
        word = "дні"
    else:
        word = "днів"

    return f"{days} {word}"