from django.db import models
from datetime import *
from django.contrib.auth.models import User


# Create your models here.
def get_file_filepath(self, filename):
	return 'import-feder/' + str(datetime.now()) + '/import.csv'

class import_dossiers(models.Model):
    import_op = models.FileField(upload_to=get_file_filepath, blank=True, null=True)
    date_import = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    def __str__(self):
        return "importation: " + str(self.date_import)

class dossier(models.Model):
    customer=models.TextField(max_length=500)
    product=models.TextField(max_length=500, default='_')
    c4c=models.TextField(max_length=500)
    channel=models.TextField(max_length=500)
    supplier=models.TextField(max_length=500)
    sample_statue=models.TextField(max_length=500)
    comm_cust=models.TextField(max_length=500)
    result_next_step=models.TextField(max_length=500)
    statue=models.TextField(max_length=500)
    y_mb=models.FloatField()
    y_vol=models.FloatField()
    vol_po_kg=models.FloatField()
    ref_prod_sap=models.TextField(max_length=500)
    prix_kg=models.FloatField()
    rep=models.TextField(max_length=500, default="_")
    sap_id = models.TextField(max_length=500, default="_")
    started_on=models.DateField(blank=True, null=True)
    up_to_date=models.DateField(blank=True, null=True)
    other=models.TextField(max_length=500)

    def __str__(self):
       return self.customer + ':' + self.product

class Note(models.Model):
    identifier = models.TextField(max_length=50, default='_')
    note = models.TextField(max_length=1500, default='_')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)

class Todo(models.Model):
    content = models.TextField(max_length=1500, default='_')
    date = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False, blank=True, null=True)
    identifier = models.TextField(max_length=50, default='_')


class Notification(models.Model):
    nature = models.TextField(max_length=1500, default='_')
    content = models.TextField(max_length=1500, default='_')
    date = models.DateField(blank=True, null=True)
    user = models.TextField(max_length=1500, default='_')
    identifier = models.TextField(max_length=1500, default='_')
    file = models.TextField(max_length=1500, default='_')
