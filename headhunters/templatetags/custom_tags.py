from django import template
from ..models import JobOffer

register = template.Library()

@register.simple_tag
def get_offer_by_id(offer_id):
    try:
        return JobOffer.objects.get(id=offer_id)
    except JobOffer.DoesNotExist:
        return None
