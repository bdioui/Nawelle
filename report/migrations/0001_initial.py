# Generated by Django 4.1.3 on 2022-12-05 09:54

from django.db import migrations, models
import report.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dossier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.TextField(max_length=500)),
                ('product', models.TextField(default='_', max_length=500)),
                ('c4c', models.TextField(max_length=500)),
                ('channel', models.TextField(max_length=500)),
                ('supplier', models.TextField(max_length=500)),
                ('sample_statue', models.TextField(max_length=500)),
                ('comm_cust', models.TextField(max_length=500)),
                ('result_next_step', models.TextField(max_length=500)),
                ('statue', models.TextField(max_length=500)),
                ('y_mb', models.FloatField()),
                ('y_vol', models.FloatField()),
                ('vol_po_kg', models.FloatField()),
                ('ref_prod_sap', models.TextField(max_length=500)),
                ('prix_kg', models.FloatField()),
                ('rep', models.TextField(default='_', max_length=500)),
                ('sap_id', models.TextField(default='_', max_length=500)),
                ('started_on', models.DateField(auto_now_add=True, null=True)),
                ('up_to_date', models.DateField(auto_now_add=True, null=True)),
                ('other', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='import_dossiers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('import_op', models.FileField(blank=True, null=True, upload_to=report.models.get_file_filepath)),
                ('date_import', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
            ],
        ),
    ]
