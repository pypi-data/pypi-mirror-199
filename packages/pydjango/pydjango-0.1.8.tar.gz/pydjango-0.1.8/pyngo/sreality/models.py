from django.db import models


class Estate(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    created_at = models.DateTimeField("Created date")
    price = models.FloatField("Price")
