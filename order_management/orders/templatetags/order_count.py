from django import template
from orders.models import Order

register = template.Library()


@register.simple_tag
def user_order_count(user):
    return Order.objects.filter(user=user).count()
