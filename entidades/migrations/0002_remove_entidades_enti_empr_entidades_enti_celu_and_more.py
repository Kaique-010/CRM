# Generated by Django 5.1 on 2024-08-22 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidades', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entidades',
            name='enti_empr',
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_celu',
            field=models.CharField(default='UNKNOWN', max_length=15),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_cep',
            field=models.CharField(default='00000000', max_length=8),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_cida',
            field=models.CharField(default='UNKNOWN', max_length=60),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_clie',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_cnpj',
            field=models.CharField(default='00000000000000', max_length=14),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_cpf',
            field=models.CharField(default='00000000000', max_length=11),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_ema',
            field=models.CharField(default='UNKNOWN', max_length=60),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_emai_empr',
            field=models.CharField(default='UNKNOWN', max_length=60),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_ende',
            field=models.CharField(default='UNKNOWN', max_length=60),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_esta',
            field=models.CharField(default='PR', max_length=2),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_fant',
            field=models.CharField(default='UNKNOWN', max_length=100),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_fone',
            field=models.CharField(default='00000000000', max_length=14),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_insc_esta',
            field=models.CharField(default='00000000000', max_length=11),
        ),
        migrations.AddField(
            model_name='entidades',
            name='enti_nume',
            field=models.CharField(default='0000', max_length=4),
        ),
        migrations.AlterField(
            model_name='entidades',
            name='enti_nome',
            field=models.CharField(default='UNKNOWN', max_length=100),
        ),
    ]
