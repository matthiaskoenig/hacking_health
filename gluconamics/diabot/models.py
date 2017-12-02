from django.db import models

from django.contrib.auth.models import User
# Create your models here.
from djchoices import DjangoChoices, ChoiceItem


# ===============================================================================
# Models
# ===============================================================================
class TissueChoices(DjangoChoices):
    """ Possible tissues for sampling."""
    PLASMA = ChoiceItem('plasma')
    SALVIA = ChoiceItem('salvia')


class MeasurementTypeChoices(DjangoChoices):
    """ Possible choices of measurement."""
    SINGLE = ChoiceItem('single')
    SERIES = ChoiceItem('series')


class Measurement(models.Model):
    """ Single sensor measurement. """
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    measurement_id = models.TextField(max_length=100)
    sensor_batch_id = models.TextField(max_length=100)
    glucose = models.FloatField()
    insulin = models.FloatField()
    tissue = models.TextField(TissueChoices)
    mtype = models.TextField(MeasurementTypeChoices)

    class Meta:
        unique_together = ('user', 'measurement_id')

    def __str__(self):
        return '<Measurement: %s %s [glc=%f [mM], ins=%f [pM]>' % (self.user, self.measurement_id, self.glucose, self.insulin)

    @property
    def evaluation(self):
        return "SUCCESS"
