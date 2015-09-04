from api.models import BugRecord

__author__ = 'hason'


def get_records_filter(objects, have_seen, start=0, end=None):
    if have_seen:
        result = objects.filter(have_seen=have_seen)
    else:
        result = objects.extra(where=["have_seen=false"], order_by=['created'])
    return result[start:end], result.count()


def get_records(start=0, end=None):
    result = BugRecord.objects.all()
    return BugRecord.objects.all()[start:end], result.count()


def get_one_record(record_id):
    try:
        record = BugRecord.objects.get(id=record_id)
    except BugRecord.DoesNotExist:
        record = None
    return record
