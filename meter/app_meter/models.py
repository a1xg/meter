from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return str(self.name)


class Resource(models.Model):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return str(self.name)


class Meter(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, blank=False)
    resource = models.ForeignKey(Resource, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return '/'


class Readings(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, blank=False, related_name='readings')
    absolute_value = models.IntegerField(blank=False)
    relative_value = models.IntegerField(blank=False)
    date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f'{self.date} ({self.absolute_value})'
