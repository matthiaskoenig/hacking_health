from django.db import models

from django.contrib.auth.models import User
# Create your models here.
from djchoices import DjangoChoices, ChoiceItem

# ===============================================================================
# Models
# ===============================================================================

class Measurement(models.Model):
    """ Single sensor measurement. """
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    measurement_id = models.TextField(max_length=100)
    sensor_batch_id = models.TextField(max_length=100)
    glucose = models.FloatField()
    insulin = models.FloatField()

    class Meta:
        unique_together = ('user', 'measurement_id')


    @property
    def evaluation(self):
        return "SUCCESS"
