from django.db import models

# Create your models here.
class Hamburguesa(models.Model):
    nombre = models.CharField(max_length=300)
    precio = models.IntegerField()
    descripcion =  models.TextField()
    imagen = models.URLField(max_length = 300)
    ingredientes = models.ManyToManyField('Ingrediente', related_name='hamburguesas',  blank=True)

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=300)
    descripcion =  models.TextField()