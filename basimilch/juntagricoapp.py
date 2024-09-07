from django.apps import AppConfig
from juntagrico.entity.subtypes import SubscriptionSize
from juntagrico.util import addons

import basimilch


class JuntagricoCustomSub(AppConfig):
    name = 'basimilch'
    verbose_name = "Basimilch"


addons.config.register_sub_overview('basi/cancel_or_continue.html')
addons.config.register_version(basimilch.name, basimilch.version)
