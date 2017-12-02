from django.contrib import admin

from django.contrib import admin
from .models import Measurement

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    fields = ('user', 'measurement_id', 'sensor_batch_id', 'glucose', 'insulin')
    list_display = ('user', 'measurement_id', 'sensor_batch_id', 'glucose', 'insulin')
    list_filter = ('user', )
