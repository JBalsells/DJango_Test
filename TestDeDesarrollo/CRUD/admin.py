from django.contrib import admin
from .models import Productos, Ingresos, Ventas

# Register your models here.

class ProductoTablaAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Productos,ProductoTablaAdmin)
admin.site.register(Ingresos,ProductoTablaAdmin)
admin.site.register(Ventas,ProductoTablaAdmin)