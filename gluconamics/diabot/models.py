from django.db import models

from collections import namedtuple
from django.contrib.auth.models import User
# Create your models here.
from djchoices import DjangoChoices, ChoiceItem

M_CUT_IGT = 40
M_CUT_T2DM = 15

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
    def t2dm_status(self):
        value = 1.0*self.insulin/self.glucose
        if value > M_CUT_IGT:
            return "normal"
        elif value < M_CUT_T2DM:
            return "t2dm"
        else:
            return "igt"

class StatusChoices(DjangoChoices):
    GOOD = ChoiceItem("good")
    NORMAL = ChoiceItem("normal")
    BAD = ChoiceItem("bad")
    DANGER = ChoiceItem("danger")


class DirectionChoices(DjangoChoices):
    CONSTANT = ChoiceItem("constant")
    IMPROVING = ChoiceItem("improving")
    WORSENING = ChoiceItem("worsening")


class InterventionChoices(DjangoChoices):
    DIET = ChoiceItem("diet")
    MEDICAL = ChoiceItem("medical")
    EXERCISE = ChoiceItem("exercise")
    MISC = ChoiceItem("misc")


class Recommendation(models.Model):
    """ Recommendation """
    recommendation_id = models.TextField()
    status = models.TextField(StatusChoices)
    direction = models.TextField(DirectionChoices)
    intervention = models.TextField(InterventionChoices)
    message = models.TextField()

    def __str__(self):
        return '<Recommendation (%s): %s %s>' % (self.intervention, self.status, self.direction)


################################################################################################################
'''
Definition of recommendations.
'''
RecDef = namedtuple('RecDef', ['rid', 'status', 'direction', 'intervention', 'message'])

rec_defs = [
    # GOOD
    RecDef(rid="R01", status=StatusChoices.GOOD, direction=DirectionChoices.CONSTANT, intervention=InterventionChoices.MISC,
           message="Hey mate, you are absolutely great. The levels are fine. Your diet and workout did wonders for your sugar levels. Keep it up buddy."),
    RecDef(rid="R02", status=StatusChoices.GOOD, direction=DirectionChoices.IMPROVING, intervention=InterventionChoices.MISC,
           message="Big improvements. You are top of the class!"),
    RecDef(rid="R03", status=StatusChoices.GOOD, direction=DirectionChoices.WORSENING, intervention=InterventionChoices.MISC,
           message="Your values decreased from the last measurement. Why not try to take the steps instead of elevators the next weeks?"),

    # NORMAL
    RecDef(rid="R04", status=StatusChoices.NORMAL, direction=DirectionChoices.CONSTANT, intervention=InterventionChoices.MISC,
           message="Your sugar levels are under control. Keep it up buddy."),
    RecDef(rid="R05", status=StatusChoices.NORMAL, direction=DirectionChoices.IMPROVING, intervention=InterventionChoices.MISC,
           message="Your levels improved. Everything is in the normal range. You are on the right track"),
    RecDef(rid="R06", status=StatusChoices.NORMAL, direction=DirectionChoices.WORSENING, intervention=InterventionChoices.DIET,
           message="Your levels decreased. How about cutting down on the sugar?"),

    # BAD
    RecDef(rid="R07", status=StatusChoices.BAD, direction=DirectionChoices.CONSTANT, intervention=InterventionChoices.EXERCISE,
           message="Nothing changed. We could try something new. How about taking a walk?"),
    RecDef(rid="R08", status=StatusChoices.BAD, direction=DirectionChoices.IMPROVING, intervention=InterventionChoices.EXERCISE,
           message="Hey mate, i think you skipped your medication/exercise. Let's collect some karma and skip sodas for the week."),
    RecDef(rid="R09", status=StatusChoices.BAD, direction=DirectionChoices.WORSENING, intervention=InterventionChoices.EXERCISE,
           message="Hey mate, i think you skipped your medication/exercise. Time to take some action. How about trying those new sneakers in the wild."),

    # DANGER
    RecDef(rid="R10", status=StatusChoices.BAD, direction=DirectionChoices.CONSTANT, intervention=InterventionChoices.MEDICAL,
           message="Your values are critical. Please talk to a medical professional."),
    RecDef(rid="R11", status=StatusChoices.BAD, direction=DirectionChoices.IMPROVING, intervention=InterventionChoices.MEDICAL,
           message="Your values are critical. Please talk to a medical professional."),
    RecDef(rid="R12", status=StatusChoices.BAD, direction=DirectionChoices.WORSENING, intervention=InterventionChoices.MEDICAL,
           message="Your values are critical. Please talk to a medical professional."),

]
################################################################################################################
