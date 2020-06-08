from django.db import models

# Create your models here.


class Nation(models.Model):
    NationName = models.CharField('NationName', primary_key=True, max_length=50)
    Area = models.CharField('Area', max_length=50)
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        db_table = 'Nation'


class City(models.Model):
    CityID = models.AutoField('CityID', primary_key=True, max_length=10)
    CityName = models.CharField('CityName', blank=False, max_length=50)
    PowerTariff = models.FloatField('PowerTariff')
    NationName = models.ForeignKey('Nation', on_delete=models.CASCADE)
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        db_table = 'City'


class CityInfo(models.Model):
    CityID = models.AutoField('CityID', primary_key=True, max_length=10)
    CityName = models.CharField('CityName', blank=False, max_length=50)
    PowerTariff = models.FloatField('PowerTariff')
    NationName = models.CharField('NationName', max_length=50)
    Comment = models.TextField('Comment', max_length=50)
    NationName = models.CharField('NationName', max_length=50)
    Area = models.CharField('Area', max_length=50)

    class Meta:
        managed = False
        db_table = 'CityInfo'


class Provider(models.Model):
    ProviderName = models.CharField('ProviderName', primary_key=True, max_length=50)
    NationName = models.ForeignKey('Nation', on_delete=models.CASCADE)
    EstablishedTime = models.DateField()
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        db_table = 'Provider'
    

class Datacenter(models.Model):
    DatacenterName = models.CharField('DatacenterName', primary_key=True, max_length=50)
    DatacenterCapacity = models.IntegerField()
    DatacenterAvaliableCapacity = models.IntegerField()
    CityID = models.ForeignKey('City', on_delete=models.CASCADE)
    Comment = models.TextField('Comment', max_length=50)
    
    class Meta:
        db_table = 'Datacenter'


class DatacenterInfo(models.Model):
    DatacenterName = models.CharField('DatacenterName', primary_key=True, max_length=50)
    DatacenterCapacity = models.IntegerField()
    DatacenterAvaliableCapacity = models.IntegerField()
    CityName = models.CharField('CityName', max_length=50)
    NationName = models.CharField('Nation', max_length=50)
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        managed = False
        db_table = 'DatacenterInfo'


class Container(models.Model):
    ContainerName = models.CharField('ContainerName', primary_key=True, max_length=50)
    ContainerIP = models.CharField('ContainerIP', max_length=50)
    CreateTime = models.DateTimeField(auto_now_add=True)
    DatacenterName = models.ForeignKey('Datacenter', on_delete=models.CASCADE)
    ProviderName = models.ForeignKey('Provider', on_delete=models.CASCADE)
    LastBootTime = models.DateTimeField()
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        db_table = 'Container'


class ContainerInfo(models.Model):
    ContainerName = models.CharField('ContainerName', primary_key=True, max_length=50)
    ContainerIP = models.CharField('ContainerIP', max_length=50)
    CreateTime = models.DateTimeField(auto_now_add=True)
    LastBootTime = models.DateTimeField()
    DatacenterName = models.CharField('Datacenter', max_length=50)
    ProviderName = models.CharField('ProviderName', max_length=50)
    CityName = models.CharField('CityName', max_length=50)
    NationName = models.CharField('NationName', max_length=50)
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        managed = False
        db_table = 'ContainerInfo'


class Service(models.Model):
    ServiceName = models.CharField('ServiceName', primary_key=True, max_length=50)
    Describe = models.TextField('Describe', max_length=50)
    Container = models.ManyToManyField(Container, through='ContainerService')
    
    class Meta:
        db_table = 'Service'


class ContainerService(models.Model):
    ContainerName = models.ForeignKey('Container', on_delete=models.CASCADE)
    ServiceName = models.ForeignKey('Service', on_delete=models.CASCADE)
    StartTime = models.DateTimeField()
    Comment = models.TextField('Comment', max_length=50)

    class Meta:
        db_table = 'ContainerService'
