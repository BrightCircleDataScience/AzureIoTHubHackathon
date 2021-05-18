from django.db import models


# Create your models here.
class MapData(models.Model):
    """This class represents the bucketlist model."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class DataPoint(models.Model):
    # in degrees celsius
    temperature = models.FloatField()
    # This is a percentage
    humidity = models.IntegerField()
    # micrograms per cubic meter
    particulates = models.FloatField()
    # 10-500 ppm
    volatile_organic_compounds = models.IntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    altitude = models.FloatField()
    # time stamp
    time_taken = models.DateTimeField()
    # processed boolean
    processed = models.BooleanField(default=False)


class jsonFeature(models.Model):
    processed_time = models.DateTimeField(null=True)
    jsonString = models.TextField()
    time_taken = models.DateTimeField()
