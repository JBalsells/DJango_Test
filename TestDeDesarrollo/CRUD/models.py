from distutils.command.upload import upload
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.utils import timezone

# Create your models here.

class Productos(models.Model):
    Pais = models.CharField(max_length=50)
    TipoDeProducto = models.CharField(max_length=50)
    NombreProducto = models.CharField(max_length=75)
    PrecioUnitario = models.FloatField()
    FechaPrecio = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
    def __str__(self):
        return self.NombreProducto

class Ingresos(models.Model):
    NombreProducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    #NombreProducto = models.CharField(max_length=75)
    CantidadIngresada = models.IntegerField()
    FechaDeIngreso = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"

    def __str__(self):
        return 'Nombre Producto: %s, Cantidad Ingresada: %s, Fecha de Ingreso: %s' % (self.NombreProducto, self.CantidadIngresada, self.FechaDeIngreso)

class Ventas(models.Model):
    NombreProducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    #NombreProducto = models.CharField(max_length=75)
    UnidadesVendidas = models.IntegerField()
    NumeroSemana = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return 'Nombre Producto: %s, Unidades Vendidas: %s, Numero Semana: %s' % (self.NombreProducto, self.UnidadesVendidas, self.NumeroSemana)