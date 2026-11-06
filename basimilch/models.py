from django.db import models
from juntagrico.entity.depot import Depot


class DepotDeliveryOptions(models.Model):
    depot = models.OneToOneField(Depot, on_delete=models.CASCADE, related_name='delivery_options')
    allows_longer_intervals = models.BooleanField(
        'Längere Lieferintervalle erlaubt', default=False,
        help_text='Erlaubt Abo-Typen, die nicht wöchentlich geliefert werden (Intervall grösser als 1 Woche).'
    )

    def __str__(self):
        return f'Lieferoptionen {self.depot}'

    class Meta:
        verbose_name = 'Lieferoptionen'
        verbose_name_plural = 'Lieferoptionen'
