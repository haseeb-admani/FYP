from django.db import models
from datetime import date

import pandas
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only CSV files are accepted.')


class PatientNotes(models.Model):
    case_num = models.CharField(max_length=10, null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    record_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.record_date)


class CsvUpload(models.Model):
    file = models.FileField(
        upload_to='csv_files/', validators=[validate_file_extension], null=True, blank=True)


@receiver(post_save, sender=CsvUpload)
def create_entries(sender, instance, **kwargs):
    # if instance.rss_link:
    #     df = fp.parse(instance.rss_link)
    # elif instance.rss_file:
    print(instance)
    data = pandas.read_csv(instance.file)
    # print(data)
    # all_rss = []
    print(data.index)
    today = date.today()
    for row in data.itertuples():
        # print(row)
        print(row.case_num)
        if(row.pn_history.strip() == ""):
            continue
        pn = PatientNotes.objects.create(
            case_num=row.case_num, history=row.pn_history, record_date=today)
        print(pn.record_date)
        pn.save()
