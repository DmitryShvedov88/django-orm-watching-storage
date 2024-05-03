import datetime
import django.utils.timezone


def format_duration(duration):
    duration = int((duration.total_seconds())//1)
    duration = str(datetime.timedelta(seconds=duration))
    return duration


def count_duration(leaved_at, entered_at):
    if leaved_at:
        leaved_at = django.utils.timezone.localtime(leaved_at)
        duration = leaved_at-entered_at
    else:
        localtime = django.utils.timezone.localtime()
        duration = localtime-entered_at 
    return duration


def get_duration(visit):
    entered_at = visit.entered_at
    entered_at = django.utils.timezone.localtime(entered_at)
    leaved_at = visit.leaved_at
    duration = count_duration(leaved_at, entered_at)
    duration = format_duration(duration)
    return duration


def is_visit_long(visit, minutes=60):
    entered_at = visit.entered_at
    entered_at = django.utils.timezone.localtime(entered_at)
    leaved_at = visit.leaved_at
    duration = count_duration(leaved_at,  entered_at)
    duration = int((duration.total_seconds())//minutes)
    return duration > 60
