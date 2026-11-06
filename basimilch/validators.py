from django.core.exceptions import ValidationError
from juntagrico.entity.subtypes import SubscriptionType


def quantity_error(form):
    """
    validates the selected quantities for Basimilch's usecase
    selected is a dictionnary with SubscriptionType objects as keys and amounts as values
    """
    present4 = 0
    present8 = 0
    present2 = 0

    if hasattr(form, 'subscription'):
        active_parts = form.subscription.active_and_future_parts
        present4 = active_parts.filter(type__bundle__product_sizes__units=4).count()
        present8 = active_parts.filter(type__bundle__product_sizes__units=8).count()
        present2 = active_parts.filter(type__bundle__product_sizes__units=2).count()

    selected = form.get_selected()
    selected4 = sum(selected[selection_type] for selection_type in SubscriptionType.objects.filter(bundle__product_sizes__units=4))
    selected8 = sum(selected[selection_type] for selection_type in SubscriptionType.objects.filter(bundle__product_sizes__units=8))
    selected2 = sum(selected[selection_type] for selection_type in SubscriptionType.objects.filter(bundle__product_sizes__units=2))

    totalNew4 = present4 + selected4
    totalNew8 = present8 + selected8
    totalNew2 = present2 + selected2

    total_liters = totalNew4 * 4 + totalNew8 * 8 + totalNew2 * 2
    if total_liters == 2:
        raise ValidationError("Falls ein Abo gewünscht ist, müssen mindestens 4 Liter in einem Abo sein.")
    required8 = total_liters // 8
    required4 = (total_liters % 8) // 4
    if not (totalNew8 == required8 and totalNew4 == required4):
        raise ValidationError(
            "Musst immer die grösstmögliche Abogrösse nehmen. "
            "Es ist zum Beispiel nicht möglich, 8 Liter auf zwei Vierliter-Abos aufzuteilen."
        )


def depot_interval_error(form):
    """
    validates that newly ordered or changed parts with a longer delivery interval
    are only added to subscriptions at depots that allow them (also for a pending depot change).
    During signup there is no subscription yet, the depot is checked by basimilch.sessions.SignupManager.
    """
    from basimilch.depot_rules import check_depot_allows

    if hasattr(form, 'part'):
        # change form: the newly chosen type replaces form.part
        type_id = getattr(form, 'cleaned_data', {}).get('part_type')
        if not type_id:
            return
        new_types = [SubscriptionType.objects.get(pk=type_id)]
        subscription = form.part.subscription
    else:
        new_types = [sub_type for sub_type, amount in form.get_selected().items() if amount]
        subscription = getattr(form, 'subscription', None)
    if subscription is None:
        return
    for depot in filter(None, [subscription.depot, subscription.future_depot]):
        check_depot_allows(depot, new_types)
