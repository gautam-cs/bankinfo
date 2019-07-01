from django.db import models


# Create your models here.
class Banks(models.Model):
    bank_name = models.CharField(max_length=50, blank=False, null=False)
    bank_id = models.BigIntegerField(blank=False, primary_key=True)

    class Meta:
        ordering = ('bank_id',)


class Branches(models.Model):
    ifsc = models.CharField(primary_key=True, max_length=11)
    bank_id = models.ForeignKey(Banks, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=100, null=False, blank=False)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        ordering = ('ifsc',)
