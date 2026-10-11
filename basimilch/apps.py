from django.apps import AppConfig


class BasimilchAppConfig(AppConfig):
    name = "basimilch"
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from juntagrico.forms import SubscriptionPartBaseForm
        from .validators import quantity_error
        SubscriptionPartBaseForm.validators.append(quantity_error)
