from django.shortcuts import render, HttpResponse
from CRUD.models import Ingresos, Ventas, Productos
from django.contrib.auth.decorators import permission_required
import csv, io



def inicio(request):
    return render(request, "inicio.html")




def productos(request):

    TipoProducto = Productos.objects.values("TipoDeProducto").distinct()
    NombreProducto = Productos.objects.values("NombreProducto").distinct()

    Producto = Productos.objects.all()

    for Prod in Producto:

        Ingreso = Ingresos.objects.filter(NombreProducto=Prod.id)
        Bodega = 0
        for contador in range(0,len(Ingreso)):
            Bodega += Ingreso[contador].CantidadIngresada
        Prod.Bodega = Bodega

        Venta = Ventas.objects.filter(NombreProducto=Prod.id)
        Liquidado = 0
        Semanas = list()
        for contador in range(0,len(Venta)):
            Liquidado += Venta[contador].UnidadesVendidas
            Semanas.append(Venta[contador].NumeroSemana.split("-"))
        Prod.Liquidado = Liquidado

        Prod.Venta = Prod.Liquidado*Prod.PrecioUnitario

        Ultima_Semana = sorted(Semanas, key=lambda x:x[1]).pop()
        Prod.Ultima_Semana = Ultima_Semana

    return render(request, "productos.html", {"productos": Producto, "TipoDeProducto": TipoProducto, "NombreProducto": NombreProducto})




def resultados(request):

    TipoProducto = Productos.objects.values("TipoDeProducto").distinct()
    NombreProducto = Productos.objects.values("NombreProducto").distinct()

    try:
        Valor = request.POST['type']
        Busqueda = "Tipo"
    except:
        try:
            Valor = request.POST['name']
            Busqueda = "Nombre"
        except:
            return HttpResponse("Error: Datos no ingresados en formularios")
    
    if(Busqueda=="Tipo"):
        Producto = Productos.objects.filter(TipoDeProducto=Valor)
    elif(Busqueda=="Nombre"):
        Producto = Productos.objects.filter(NombreProducto=Valor)

    for Prod in Producto:
    
        Ingreso = Ingresos.objects.filter(NombreProducto=Prod.id)
        Bodega = 0
        for contador in range(0,len(Ingreso)):
            Bodega += Ingreso[contador].CantidadIngresada
        Prod.Bodega = Bodega

        Venta = Ventas.objects.filter(NombreProducto=Prod.id)
        Liquidado = 0
        Semanas = list()
        for contador in range(0,len(Venta)):
            Liquidado += Venta[contador].UnidadesVendidas
            Semanas.append(Venta[contador].NumeroSemana.split("-"))
        Prod.Liquidado = Liquidado

        Prod.Venta = Prod.Liquidado*Prod.PrecioUnitario

        Ultima_Semana = sorted(Semanas, key=lambda x:x[1]).pop()
        Prod.Ultima_Semana = Ultima_Semana

    return render(request, "productos.html", {"productos": Producto, "TipoDeProducto": TipoProducto, "NombreProducto": NombreProducto})




def historico(request, GetId):
    ProductoFiltrado = Productos.objects.get(id=GetId)

    print(ProductoFiltrado)

    Producto = Productos.objects.values("NombreProducto", "id", "TipoDeProducto").get(NombreProducto=ProductoFiltrado)
    Datos_Ventas = Ventas.objects.values("UnidadesVendidas", "NumeroSemana").filter(NombreProducto_id=Producto['id'])

    DataList = list()
    for dato in range(0,len(Datos_Ventas)):
        Semana = int(Datos_Ventas[dato]['NumeroSemana'].split('-')[0])
        DataList.append([Datos_Ventas[dato]['UnidadesVendidas'], Semana, Datos_Ventas[dato]['NumeroSemana']])

    DataList = sorted(DataList, key=lambda x:x[1])
    print(DataList)

    return render(request, "historico.html", {"producto": ProductoFiltrado, "DataList":DataList})




def cargar(request):
    from django.http import StreamingHttpResponse
    return render(request, "cargar.html")



@permission_required('admin.can_add_log_entry')
def carga_excel(request):
    #pip install xlrd
    #pip install openpyxl
    import pandas as pd
    if request.method == "GET":
        return render(request, "cargar.html", prompt)

    try:
        excel_file = request.FILES['excel_file']
        tabla1 = pd.read_excel(excel_file, engine="openpyxl", sheet_name="tabla1")
        tabla2 = pd.read_excel(excel_file, engine="openpyxl", sheet_name="tabla2")
        tabla3 = pd.read_excel(excel_file, engine="openpyxl", sheet_name="tabla3")
    except:
        return render(request, "error.html", {"error": "Por favor, asegúrese de cumplir lo siguiente: 1) subir únicamente un archivo en formato XLSX válido con la plantilla indicada, 2) tener instalado openpyxl (pip install openpyxl)"})

    t1d = tabla1.describe()
    t2d = tabla2.describe()
    t3d = tabla3.describe()

    if not excel_file.name.endswith('xlsx'):
        return render(request, "error.html", {"error": "Por favor, asegúrese de cumplir lo siguiente: 1) subir únicamente un archivo en formato XLSX válido con la plantilla indicada, 2) tener instalado openpyxl (pip install openpyxl)"})
    return render(request, "datos_excel.html", {"tabla1":tabla1, "tabla2":tabla2, "tabla3":tabla3, "describe1":t1d, "describe2": t2d, "describe3": t3d})




@permission_required('admin.can_add_log_entry')
def carga_csv(request):
    prompt = {"orden": "El orden del csv es numero de semana, nombre de producto, tipo de producto, unidades vendidas"}

    if request.method == "GET":
        return render(request, "cargar.html", prompt)

    csv_file = request.FILES['csv_file']
    if not csv_file.name.endswith('csv'):
        return render(request, "error.html", {"error": "Por favor, subir únicamente un archivo en formato CSV válido con la plantilla indicada"})
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    Columns = list()
    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        IdProducto = Productos.objects.values("id").get(NombreProducto=column[1])
        Ventas.objects.create(NombreProducto_id=IdProducto['id'], UnidadesVendidas=column[3], NumeroSemana=column[0])
        Columns.append(column)
    return render(request, "datos_csv.html", {"CSVData":Columns})




def proyecciones(request):
    NombreProducto = Productos.objects.values("NombreProducto").distinct()
    FechaIngreso = Ventas.objects.values("NumeroSemana").all()

    fechas = set()
    for fecha in range(0,len(FechaIngreso)):
        fechas.add(FechaIngreso[fecha]['NumeroSemana'].split('-')[1])

    return render(request, "proyecciones.html", {"NombreProducto": NombreProducto, "Fechas": fechas})




def forecast(request):
    #import numpy as np
    #import pandas as pd
    from sklearn import linear_model

    NombreProducto = Productos.objects.values("NombreProducto").distinct()
    FechaIngreso = Ventas.objects.values("NumeroSemana").all()

    fechas = set()
    for fecha in range(0,len(FechaIngreso)):
        fechas.add(FechaIngreso[fecha]['NumeroSemana'].split('-')[1])

    try:
        try:
            Nombre = request.POST['name']
            Fecha = request.POST['fecha']
            Prediccion = request.POST['prediccion']
        except:
            return render(request, "error.html", {"error":"Existe un problema en el request Http con método POST de envío de datos al controlador."})
        Producto = Productos.objects.values("NombreProducto", "id", "TipoDeProducto").get(NombreProducto=Nombre)
        Datos_Ventas = Ventas.objects.values("UnidadesVendidas", "NumeroSemana").filter(NumeroSemana__contains=Fecha).filter(NombreProducto_id=Producto['id'])

        DataList = list()
        for dato in range(0,len(Datos_Ventas)):
            Semana = int(Datos_Ventas[dato]['NumeroSemana'].split('-')[0])
            DataList.append([Datos_Ventas[dato]['UnidadesVendidas'], Semana])

        DataList = sorted(DataList, key=lambda x:x[1])

        XData = list()
        YData = list()
        for dato in range(0, len(DataList)):
            XData.append([DataList[dato][1]])
            YData.append(DataList[dato][0])

        regr = linear_model.LinearRegression()
        regr.fit(XData, YData)
        const = [regr.coef_,regr.intercept_]

        Y_Pred = regr.predict([[float(Prediccion)]])
        print(Y_Pred)

        return render(request, "proyecciones.html", {"NombreProducto": NombreProducto, "Fechas": fechas, "producto":Producto, "constantes":const, "data": DataList, "Prediccion": [Prediccion, Y_Pred]})
    except:
        return render(request, "error.html", {"error": "Por favor revise lo siguiente: 1) tener instalado sklearn, 2)Llenar todos los campos del formulario, 3) El mes a predecir debe ser un numero entero o real."})