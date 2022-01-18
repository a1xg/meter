from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=50, blank=False)


class Counter(models.Model):
    unit = models.CharField(max_length=10, blank=False)
    name = models.CharField(max_length=200, blank=False)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)


class Record(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, blank=False)
    absolute_value = models.IntegerField(blank=False)
    relative_value = models.IntegerField(blank=False)
    date = models.DateField(auto_now_add=True)
