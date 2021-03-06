# Generated by Django 2.1 on 2020-06-07 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityInfo',
            fields=[
                ('CityID', models.AutoField(max_length=10, primary_key=True, serialize=False, verbose_name='CityID')),
                ('CityName', models.CharField(max_length=50, verbose_name='CityName')),
                ('PowerTariff', models.FloatField(verbose_name='PowerTariff')),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
                ('NationName', models.CharField(max_length=50, verbose_name='NationName')),
                ('Area', models.CharField(max_length=50, verbose_name='Area')),
            ],
            options={
                'db_table': 'CityInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContainerInfo',
            fields=[
                ('ContainerName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='ContainerName')),
                ('ContainerIP', models.CharField(max_length=50, verbose_name='ContainerIP')),
                ('CreateTime', models.DateTimeField(auto_now_add=True)),
                ('LastBootTime', models.DateTimeField()),
                ('DatacenterName', models.CharField(max_length=50, verbose_name='Datacenter')),
                ('ProviderName', models.CharField(max_length=50, verbose_name='ProviderName')),
                ('CityName', models.CharField(max_length=50, verbose_name='CityName')),
                ('NationName', models.CharField(max_length=50, verbose_name='NationName')),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
            ],
            options={
                'db_table': 'ContainerInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DatacenterInfo',
            fields=[
                ('DatacenterName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='DatacenterName')),
                ('DatacenterCapacity', models.IntegerField()),
                ('DatacenterAvaliableCapacity', models.IntegerField()),
                ('CityName', models.CharField(max_length=50, verbose_name='CityName')),
                ('NationName', models.CharField(max_length=50, verbose_name='Nation')),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
            ],
            options={
                'db_table': 'DatacenterInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('CityID', models.AutoField(max_length=10, primary_key=True, serialize=False, verbose_name='CityID')),
                ('CityName', models.CharField(max_length=50, verbose_name='CityName')),
                ('PowerTariff', models.FloatField(verbose_name='PowerTariff')),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
            ],
            options={
                'db_table': 'City',
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('ContainerName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='ContainerName')),
                ('ContainerIP', models.CharField(max_length=50, verbose_name='ContainerIP')),
                ('CreateTime', models.DateTimeField(auto_now_add=True)),
                ('LastBootTime', models.DateTimeField()),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
            ],
            options={
                'db_table': 'Container',
            },
        ),
        migrations.CreateModel(
            name='ContainerService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartTime', models.DateTimeField()),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
                ('ContainerName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Container')),
            ],
            options={
                'db_table': 'ContainerService',
            },
        ),
        migrations.CreateModel(
            name='Datacenter',
            fields=[
                ('DatacenterName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='DatacenterName')),
                ('DatacenterCapacity', models.IntegerField()),
                ('DatacenterAvaliableCapacity', models.IntegerField()),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
                ('CityID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.City')),
            ],
            options={
                'db_table': 'Datacenter',
            },
        ),
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('NationName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='NationName')),
                ('Area', models.CharField(max_length=50, verbose_name='Area')),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
            ],
            options={
                'db_table': 'Nation',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('ProviderName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='ProviderName')),
                ('EstablishedTime', models.DateField()),
                ('Comment', models.TextField(max_length=50, verbose_name='Comment')),
                ('NationName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Nation')),
            ],
            options={
                'db_table': 'Provider',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('ServiceName', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='ServiceName')),
                ('Describe', models.TextField(max_length=50, verbose_name='Describe')),
                ('Container', models.ManyToManyField(through='api.ContainerService', to='api.Container')),
            ],
            options={
                'db_table': 'Service',
            },
        ),
        migrations.AddField(
            model_name='containerservice',
            name='ServiceName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Service'),
        ),
        migrations.AddField(
            model_name='container',
            name='DatacenterName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Datacenter'),
        ),
        migrations.AddField(
            model_name='container',
            name='ProviderName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Provider'),
        ),
        migrations.AddField(
            model_name='city',
            name='NationName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Nation'),
        ),
    ]
