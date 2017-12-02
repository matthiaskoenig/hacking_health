from django.contrib import admin

from django.contrib import admin
from .models import Measurement

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    fields = ('user', 'timestamp', 'measurement_id', 'sensor_batch_id', 'glucose', 'insulin')
