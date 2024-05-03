from django.shortcuts import render, get_object_or_404
from datacenter.models import Passcard
from datacenter.models import Visit
from calculating_visit_time import get_duration, is_visit_long

def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = [
        {
            'entered_at': str(visit.entered_at),
            'duration': get_duration(visit),
            'is_strange': is_visit_long(visit, minutes=60)
        }
        for visit in visits
    ]
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
