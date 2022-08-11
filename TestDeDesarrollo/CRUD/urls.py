from django.urls import path

from CRUD import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('productos', views.productos, name="productos"),
    path('cargar', views.cargar, name="cargar"),
    path('proyecciones', views.proyecciones, name="proyecciones"),


    path('historico/<GetId>', views.historico, name="historico"),
    path('resultados/', views.resultados, name="resultados"),

    path('carga_csv/', views.carga_csv, name="carga_csv"),
    path('carga_excel/', views.carga_excel, name="carga_excel"),

    path('forecast/', views.forecast, name="forecast"),
]
