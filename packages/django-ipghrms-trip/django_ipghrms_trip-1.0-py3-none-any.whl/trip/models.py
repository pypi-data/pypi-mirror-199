from django.db import models
from custom.models import Country, Municipality
from django.contrib.auth.models import User
from employee.models import Employee
from settings_app.upload_utils import upload_trip
from django.core.validators import FileExtensionValidator

class TripType(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name
        
    

class Trip(models.Model):
    name = models.CharField(max_length=100, null=True)
    date_out = models.DateField(null=False, verbose_name="Data Sai",blank=True)
    date_in = models.DateField(null=False, verbose_name="Data Tama",blank=True)
    ttype = models.ForeignKey(TripType, null=True, blank=True, on_delete=models.CASCADE, related_name='triptype', verbose_name="Trip Type")
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Nasaun")
    municipality = models.ForeignKey(Municipality, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Municipio")
    file = models.FileField(upload_to=upload_trip, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Upload PDF")
    is_lock = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=32, null=True,blank=True)

    def __str__(self):
        return self.name

class TripEmp(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tripemp', verbose_name="Pessoal")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, verbose_name="Trip")
    is_lock = models.BooleanField(default=True, null=True, blank=True, verbose_name="Chave")
    is_update = models.BooleanField(default=False, null=True, blank=True, verbose_name="Update Absensia")
    datetime = models.DateTimeField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hashed = models.CharField(max_length=32, null=True,blank=True)
    def __str__(self):
        template = '{0.employee} - {0.trip}'
        return template.format(self)
    