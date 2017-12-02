from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Measurement


@login_required
def index_view(request):
    measurements = Measurement.objects.filter(user=request.user)
    context = {
        'measurements': measurements,
    }
    return render(request,
                  'glucoonamics/index.html', context)
