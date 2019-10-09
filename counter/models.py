from django.db import models
import datetime
from django.utils import timezone

class Counter(models.Model):
    record = models.DateTimeField('record')
    passed = models.IntegerField('passed')
    class Meta:
        db_table = 'counter'
        managed = False