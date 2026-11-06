"""
Basimilch rule: subscription types that are not delivered weekly (interval > 1)
are only available at depots that allow longer intervals (see DepotDeliveryOptions).
"""
from django.core.exceptions import ValidationError

from basimilch.models import DepotDeliveryOptions


def has_longer_interval(subscription_types):
    return any(sub_type.interval > 1 for sub_type in subscription_types)


def allows_longer_intervals(depot):
    return DepotDeliveryOptions.objects.filter(depot=depot, allows_longer_intervals=True).exists()


def depot_allows(depot, subscription_types):
    return not has_longer_interval(subscription_types) or allows_longer_intervals(depot)


def error_message(depot):
    return f'Im Depot {depot} sind nur wöchentlich gelieferte Abos möglich.'


def check_depot_allows(depot, subscription_types):
    if not depot_allows(depot, subscription_types):
        raise ValidationError(error_message(depot), code='depot_interval')
