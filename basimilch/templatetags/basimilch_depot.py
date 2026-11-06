from django import template
from juntagrico.entity.subtypes import SubscriptionType

from basimilch.depot_rules import depot_allows

register = template.Library()


@register.simple_tag
def depot_unavailable(depot, subscription_count=None):
    """
    True if the depot does not allow the given subscription types.
    subscription_count: {type_id: amount}, as passed by juntagrico to the depot selection
    (string keys from the signup session, integer keys on the depot change page)
    """
    if not subscription_count:
        return False
    type_ids = [int(type_id) for type_id, amount in subscription_count.items() if amount]
    return not depot_allows(depot, SubscriptionType.objects.filter(id__in=type_ids))
