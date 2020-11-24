import csv
import os
import timeit

def clientes_archivo():
    nombre = input("Ingrese nombre del archivo de clientes: ")
    
    while nombre == "" or nombre == None:
        nombre = input("Debe ingresar el nombre del archivo de clientes: ")
    
    return f"{nombre}"

def viaticos_archivo():
    nombre = input("Ingrese nombre del archivo de viáticos: ")
    
    while nombre == "" or nombre == None:
        nombre = input("Debe ingresar el nombre del archivo de viáticos: ")
    
    return f"{nombre}"

def abrir_archivo(nombre_archivo):
    try:
        open(nombre_archivo)
        print(f"Ok: El archivo {nombre_archivo} se ha encontrado!")
    except IOError:
        print(f"ERROR: El archivo {nombre_archivo} no se ha encontrado!")
        exit()

def opcion_1(in_nombre, csv_clientes, coincidencias, linea):  
    # # Time:  0.01869909999999919
    for Nombre, Dirección, Documento, Fecha, Correo, Empresa in csv_clientes:
        if in_nombre in Nombre.lower():
            print("{}\nCliente: {}\n{}\nDirección: {}\nDNI: {}\nFecha de alta: {}\nCorreo Electrónico: {}\nEmpresa: {}\n".format(linea, Nombre, linea, Dirección, Documento, Fecha, Correo, Empresa))
            coincidencias = True
            
    if coincidencias == False:
        print("No se encontraron coincidencias")

def opcion_2(in_empresa, lista_empresa_actual, coincidencias, linea):
               
    # Time:  0.019830999999999932
    for Nombre, Dirección, Documento, Fecha, Correo, Empresa in lista_empresa_actual:
        # se consideran los nombres de los campos
        if len(lista_empresa_actual) > 1:
            if coincidencias == False:
                print(f"{linea}\nEmpresa: {in_empresa}.\nTotal Usuarios: {(len(lista_empresa_actual)-1)}\n{linea}")
                coincidencias = True
            print(f"[{Nombre}, {Dirección}, {Documento}, {Fecha}, {Correo}, {Empresa}]")
        else:
            print("No se encontraron coincidencias")
    
def opcion_3(csv_viaticos, lista_empresa_actual, in_empresa, linea):
    total = 0
    contador = 0 
         
    try:
        for viaje in csv_viaticos:
            monto = (viaje[2]).replace(",", "")
            f_monto = float(monto)
            for cliente in lista_empresa_actual:
                if viaje[0] == cliente[0] and cliente[1] == in_empresa:
                    contador += 1
                    total += f_monto
                else:
                    pass
    except ValueError:
        print("ERROR: No se pudo hacer el cálculo")
        pass
    
    if contador >= 1:
        total = '{:.2f}'.format(total)
        print(f"{linea}\n{in_empresa}. ${total} \n{linea}" );
    else:
        print("No se encontraron coincidencias")

def opcion_4(lista_cliente, csv_viaticos, in_dni, cabecera_cliente, cabecera_viajes, linea):

    total = 0
    cantidad = 0
    viajes = []

    if len(lista_cliente) == 0:
        print("No se encontraron coincidencias")
    else:
        try:                      
            for viaje in csv_viaticos:
                Documento, fecha, monto = viaje
                if Documento == in_dni:
                    viajes.append(viaje)
                    monto_aux = (monto).replace(",", "")
                    f_monto = float(monto_aux)
                    cantidad += 1
                    total += f_monto
            print(f"{linea}\n{in_dni}\n{linea}")
            
            total = '{:.2f}'.format(total)
                        
            for Nombre, Dirección, Documento, Fecha, Correo, Empresa in cabecera_cliente:
                print("[{}, {}, {}, {}, {}, {}]".format(Nombre, Dirección, Documento, Fecha, Correo, Empresa))
                
            for cliente in lista_cliente:
                Nombre, Dirección, Documento, Fecha, Correo, Empresa = cliente.rstrip("\n").split(',')
                print("[{}]".format(cliente))
            
            print(f"{linea}\nTotal viajes: {cantidad}, Monto: ${total}\n{linea}")
            
            for Documento, fecha, monto in cabecera_viajes:
                print("[{}, {}, {}]".format(Documento, fecha, monto))
                
            for Documento, fecha, monto in viajes:
                print("[{}, {}, {}]".format(Documento, fecha, monto))

        except:
            print("No se pudo traer la información.")
            pass

def escribir_log(tipo_log):
    nombre_log = "sys_clientes.log"
    
    try:
        open(nombre_log)
        with open(nombre_log, "a", newline="") as f_log:
            csv_log = csv.writer(f_log)
            nuevo_log = tipo_log
            csv_log.writerow([nuevo_log])
    except FileNotFoundError:
        with open(nombre_log, "w", newline="") as f_log:
            csv_log = csv.writer(f_log)
            cabecera = "Acción"
            csv_log.writerow([cabecera])
            csv_log.writerow(["Menú"])
            print("Archivo log creado con exito en ", os.path.abspath(nombre_log))     
        
def busqueda(archivo_clientes, archivo_viaticos, opcion):
    
    with open("Clientes.csv", 'r', encoding="utf-8") as f_clientes:
        csv_clientes = csv.reader(f_clientes, delimiter=",")
        linea = '-'*78
        coincidencias = False
        viaticos = 0

        if opcion == 1:
            tipo_log = "Búsqueda de cliente por nombre"
            next(csv_clientes)
            in_nombre = input("Ingrese nombre a buscar: ")
            
            while in_nombre == "":
                in_nombre = input("No se acepta un ingreso vacío\nIngrese un nombre para buscar: ")
                
            opcion_1(in_nombre, csv_clientes, coincidencias, linea)
                            
            escribir_log(tipo_log)
                
        elif opcion == 2:
            tipo_log = "Búsqueda total usuarios por empresa"
            
            in_empresa = input("Ingrese empresa a buscar: ") 
                
            while in_empresa == "":
                in_empresa = input("No se acepta un ingreso vacío\nIngrese un nombre para buscar: ")

            # Time:  0.000547499999999701
            lista_empresas = list(csv_clientes)         
            lista_empresa_actual = [[Nombre, Dirección, Documento, Fecha, Correo, Empresa] for Nombre, Dirección, Documento, Fecha, Correo, Empresa in lista_empresas if Empresa == in_empresa or Nombre == "Nombre"]
            opcion_2(in_empresa, lista_empresa_actual, coincidencias, linea)
            
            escribir_log(tipo_log)
            
        elif opcion == 3:
            
            tipo_log = "Busqueda total viáticos por empresa"
            
            with open(archivo_viaticos, 'r', encoding="utf-8") as f_viaticos:
                csv_viaticos = csv.reader(f_viaticos, delimiter=",")
                
                lista_empresas = list(csv_clientes)
                               
                lista_empresa_actual = [[ Documento, Empresa] for Nombre, Dirección, Documento, Fecha, Correo, Empresa in lista_empresas if Nombre != "Nombre"]
                lista_empresa_actual.sort()             
                
                in_empresa = input("Ingrese empresa a buscar: ") 
                while in_empresa == "":
                    in_empresa = input("No se acepta un ingreso vacío\nIngrese una empresa para buscar: ")

                viaje = next(csv_viaticos, None)

                opcion_3(csv_viaticos, lista_empresa_actual, in_empresa, linea)
                
            escribir_log(tipo_log)
            
        elif opcion == 4:
            
            tipo_log = "Busqueda total viáticos por cliente"
            
            with open("viajes.csv", 'r', encoding="utf-8") as f_viaticos:
                csv_viaticos = csv.reader(f_viaticos, delimiter=",")
                
                cabecera_cliente = [next(csv_clientes, None)]
                cabecera_viajes = [next(csv_viaticos, None)]
                
                in_dni = input("Ingrese dni a buscar: ")
                while in_dni == "":
                    in_dni = input("No se acepta un ingreso vacío\nIngrese un Dni para buscar: ")
                
                lista_empresas = list(csv_clientes)
                
                lista_cliente = [', '.join([Nombre, Direccion, Documento, Fecha, Correo, Empresa]) for Nombre, Direccion, Documento, Fecha, Correo, Empresa in lista_empresas if Documento == in_dni]
                
                opcion_4(lista_cliente, csv_viaticos, in_dni, cabecera_cliente, cabecera_viajes, linea)
                
            escribir_log(tipo_log)

def comprobacion_viajes(nombre_archivo):
    with open(nombre_archivo, 'r', encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        lista_v_copia = list(csvreader)
        
        flag = True      
                
        viajes_monto = [[Documento, fecha, monto] for Documento, fecha, monto in lista_v_copia if (monto[::-1].find('.')) != 2 and monto != "monto"]
        if len(viajes_monto) > 0:
            print(f"ERROR: El archivo {nombre_archivo} tiene precios con formato no permitido")
            flag = False
        
        viajes_vacio = [[Documento, fecha, monto] for Documento, fecha, monto in lista_v_copia if Documento in (None, "") or fecha in (None, "") or monto in (None, "")]
        if len(viajes_vacio) > 0:
            print(f"ERROR: El archivo {nombre_archivo} tiene campos vacíos")
            flag = False
        
        viajes_dni = [[Documento, fecha, monto] for Documento, fecha, monto in lista_v_copia if len(Documento) < 7 or len(Documento) > 8 and Documento != "Documento"]
        if len(viajes_dni) > 0:
            print(f"ERROR: El archivo {nombre_archivo} tiene documentos con menos de 7 o mas de 8 caracteres")
            flag = False

        return flag

def comprobacion_clientes(nombre_archivo):

    with open(nombre_archivo, 'r', encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        lista_c_copia = list(csvreader)
       
        flag = True
        
        clientes_mail = [[Nombre, Direccion, Documento, Fecha, Correo, Empresa] for Nombre, Direccion, Documento, Fecha, Correo, Empresa in lista_c_copia if Correo.count("@") != 1 and Correo.count(".") != 1 and "Correo" not in Correo]
        if len(clientes_mail) > 0:
            print(f"ERROR: El archivo {nombre_archivo} tiene e-mails con formato no permitido")
            flag = False
        
        clientes_vacio = [[Nombre, Direccion, Documento, Fecha, Correo, Empresa] for Nombre, Direccion, Documento, Fecha, Correo, Empresa in lista_c_copia if Nombre in (None, "") or Direccion in (None, "") or Documento in (None, "") or Fecha in (None, "") or Correo in (None, "") or Empresa in (None, "")]
        if len(clientes_vacio) > 0:
            print(f"ERROR: El archivo {nombre_archivo} tiene campos vacíos")
            flag = False
        
        viajes_dni = [[Nombre, Direccion, Documento, Fecha, Correo, Empresa] for Nombre, Direccion, Documento, Fecha, Correo, Empresa in lista_c_copia if len(Documento) < 7 or len(Documento) > 8 and Documento != "Documento"]
        if len(viajes_dni) > 0:
            print(f"ERROR: El archivo {nombre_archivo} tiene documentos con menos de 7 o mas de 8 caracteres")
            flag = False

        return flag