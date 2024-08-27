# Generated by Django 5.1 on 2024-08-27 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Licencas',
            fields=[
                ('lice_id', models.AutoField(primary_key=True, serialize=False)),
                ('lice_docu', models.CharField(blank=True, max_length=60, null=True)),
                ('lice_nome', models.CharField(blank=True, max_length=60, null=True)),
                ('lice_emai', models.CharField(blank=True, max_length=150, null=True)),
                ('lice_nume_maqu', models.IntegerField(blank=True, null=True)),
                ('lice_bloq', models.BooleanField(blank=True, null=True)),
                ('lice_nume_empr', models.IntegerField(blank=True, null=True)),
                ('lice_nume_fili', models.IntegerField(blank=True, null=True)),
                ('field_log_data', models.DateField(blank=True, db_column='_log_data', null=True)),
                ('field_log_time', models.TimeField(blank=True, db_column='_log_time', null=True)),
            ],
            options={
                'db_table': 'licencas',
                'managed': False,
            },
        ),
    ]
