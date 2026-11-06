from django.contrib import admin
from juntagrico.entity.depot import Depot
from juntagrico.util import addons

from basimilch.models import DepotDeliveryOptions


class DepotDeliveryOptionsInline(admin.StackedInline):
    model = DepotDeliveryOptions
    can_delete = False


# registered here and not in AppConfig.ready, because juntagrico's admin is set up before basimilch is ready.
# admin modules are imported in the order of INSTALLED_APPS, where basimilch comes before juntagrico.
addons.config.register_model_inline(Depot, DepotDeliveryOptionsInline)
