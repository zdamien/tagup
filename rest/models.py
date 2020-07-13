from django.db import models
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse

import json
import time

V1_LEN = 10  #testing value
#V1_LEN = 4096  #real-world value?

class Record(models.Model):
    #Django recommends against using __init__ for Model classes.

    # id field is inherited from Model and set by the database.
    timestamp = models.BigIntegerField() #times are Unix epoch in milliseconds
    value1 = models.CharField(max_length=V1_LEN) 
    value2 = models.FloatField() 
    value3 = models.BooleanField() 
    #These two are set by an overidden save() method:
    creationDate = models.BigIntegerField(default=-1)
    lastModificationDate = models.BigIntegerField()

    def create(ts=0, v1="", v2=0.0, v3=False):
        assert isinstance(ts, int)
        assert isinstance(v1, str)
        assert isinstance(v2, float)
        assert isinstance(v3, bool)
        r = Record()
        r.timestamp = ts
        r.value1 = v1
        r.value2 = v2
        r.value3 = v3
        return r

    def save(self, *args, **kwargs):
        """Overriding super.save() to get timestamp fields in the DB.
        DB definition would be better -- at my last job we had
        create_time and modify_time set by MySQL definitions -- but
        sqlite3 is simple, as is my knowledge of it."""

        now = int( time.time() * 1000 )
        if self.creationDate == -1:
            self.creationDate = now
        self.lastModificationDate = now
        return super(Record, self).save(*args, **kwargs)

    def __str__(self):
        if self.id is None: return "No id"
        return str(self.id)

    def to_dict(self):
        d = dict()
        d["id"] = self.id
        d["timestamp"] = self.timestamp
        d["value1"] = self.value1
        d["value2"] = self.value2
        d["value3"] = self.value3
        return d

    def to_json(self):
        d = self.to_dict()
        return json.dumps(d)
    
    def to_debug(self):
        d = self.to_dict()
        d["creationDate"] = self.creationDate
        d["lastModificationDate"] = self.lastModificationDate
        return json.dumps(d)

    
def list(request):
    "Returns list of ids."

    recs = get_list_or_404(Record)
    l = []
    for r in recs:
        l.append(r.id)
    return HttpResponse(json.dumps(l))

@csrf_exempt
def create(request):
    body = request.read().decode()
    d = json.loads(body)
    timestamp = int(d["timestamp"])
    if len(d["value1"]) > V1_LEN:
        return HttpResponse(status=400, reason="value1 too long.")
    value1 = d["value1"]
    value2 = float(d["value2"])
    value3 = bool(d["value3"])

    record = Record.create(timestamp, value1, value2, value3)
    record.save()
    return HttpResponse(record.to_json())

def read(request, recordId):
    record = get_object_or_404(Record, pk=recordId)
    return HttpResponse(record.to_json())

def debug(request, recordId):
    "Like read but also returns create and modify fields."
    record = get_object_or_404(Record, pk=recordId)
    return HttpResponse(record.to_debug())

@csrf_exempt
def modify(request, recordId):
    record = get_object_or_404(Record, pk=recordId)

    body = request.read().decode()
    d = json.loads(body)
    if 'timestamp' in d:
        record.timestamp = int(d['timestamp'])
    if 'value1' in d:
        if len(d["value1"]) > V1_LEN:
            return HttpResponse(status=400, reason="value1 too long.")
        record.value1 = d['value1']
    if 'value2' in d:
        record.value2 = float(d['value2'])
    if 'value3' in d:
        record.value3 = bool(d['value3'])
    record.save()
    return HttpResponse(record.to_json())

@csrf_exempt
def remove(request, recordId):
    record = get_object_or_404(Record, pk=recordId)
    record.delete()
    return HttpResponse("Deleted.")
