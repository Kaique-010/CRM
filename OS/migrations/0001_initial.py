# Generated by Django 5.1 on 2024-08-26 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdemServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serv_empr', models.IntegerField()),
                ('serv_fili', models.IntegerField()),
                ('serv_os', models.CharField(max_length=20)),
                ('os_data_aber', models.DateField()),
                ('os_data_fech', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ordem_servico',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pecaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peca_item', models.IntegerField()),
                ('peca_quan', models.FloatField()),
                ('peca_unit', models.FloatField()),
                ('peca_desc', models.FloatField()),
                ('peca_tota', models.FloatField()),
            ],
            options={
                'verbose_name': 'Peça',
                'verbose_name_plural': 'Peças',
                'db_table': 'pecasos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serv_item', models.IntegerField()),
                ('serv_quan', models.FloatField()),
                ('serv_unit', models.FloatField()),
                ('serv_desc', models.FloatField()),
                ('serv_tota', models.FloatField()),
            ],
            options={
                'verbose_name': 'Serviço',
                'verbose_name_plural': 'Serviços',
                'db_table': 'servicosos',
                'managed': False,
            },
        ),
    ]
