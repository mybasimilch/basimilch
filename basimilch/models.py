from django.db import models


class DepotlistView(models.Model):
    depot = models.CharField("Depot", max_length=100, primary_key=True)
    wochentag = models.IntegerField("Wochentag")
    fruchtjoghurt = models.IntegerField("Fruchtjoghurt")
    naturejoghurt = models.IntegerField("naturejoghurt")
    quark = models.IntegerField("Quark")
    rohmilch = models.IntegerField("Rohmilch")
    wochenkaese_gross_1 = models.IntegerField("Wochenkäse gross 1")
    wochenkaese_gross_2 = models.IntegerField("Wochenkäse gross 2")
    wochenkaese_klein = models.IntegerField(("Wochenkäse klein"))
    zusatzkaese = models.IntegerField("Zusatzkäse")

    class Meta:
        managed = False
        db_table = "depotlist_view"
