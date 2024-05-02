import datetime
from django.db import models
import django.utils.timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def format_duration(duration):
    duration = int((duration.total_seconds())//1)
    duration = str(datetime.timedelta(seconds=duration))
    return duration


def get_duration(visit):
    entered_at = visit.entered_at
    entered_at = django.utils.timezone.localtime(entered_at)
    leaved_at = visit.leaved_at
    if leaved_at:
        leaved_at = visit.leaved_at
        leaved_at = django.utils.timezone.localtime(leaved_at)
        duration = leaved_at-entered_at
    else:
        localtime = django.utils.timezone.localtime()
        duration = localtime-entered_at  
    duration = format_duration(duration)
    return duration


def is_visit_long(visit, minutes=60):
    entered_at = visit.entered_at
    entered_at = django.utils.timezone.localtime(entered_at)
    leaved_at = visit.leaved_at
    if leaved_at:
        leaved_at = visit.leaved_at
        leaved_at = django.utils.timezone.localtime(leaved_at)
        duration = leaved_at-entered_at
    else:
        localtime = django.utils.timezone.localtime()
        duration = localtime-entered_at
    duration = int((duration.total_seconds())//minutes)
    if duration > 60:
        return True
    else:
        return False
