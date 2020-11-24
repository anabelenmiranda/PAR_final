import funciones
import os

def menu():
    
    archivo_clientes = funciones.clientes_archivo()
    funciones.abrir_archivo(archivo_clientes)
   
    archivo_viaticos = funciones.viaticos_archivo() 
    funciones.abrir_archivo(archivo_viaticos)
    
    if funciones.comprobacion_clientes(archivo_clientes) == False or funciones.comprobacion_viajes(archivo_viaticos) == False:
        print("No se puede seguir con la ejecución...")
        exit()
        
    while True:
        tipo_log = "Menú"
        funciones.escribir_log(tipo_log)
        
        opcion = input("*** MENU ***\n1- Buscar cliente\n2- Busqueda de usuarios por Empresa\n3- Total de viaticos por Empresa\n4- Viajes por Cliente\n5- Salir\n")
        # Opcion 1: Buscar nombre de cliente
        if opcion == "1":
            funciones.busqueda(archivo_clientes, archivo_viaticos, 1)
        
        # Opcion 2: Buscar Usuario por Empresa
        elif opcion == "2":
            funciones.busqueda(archivo_clientes, archivo_viaticos, 2)
        
        # Opcion 3: Total viaticos por Empresa
        elif opcion == "3":
            funciones.busqueda(archivo_clientes, archivo_viaticos, 3)
        
        # Ocion 4: Total viaticos por Cliente
        elif opcion == "4":
            funciones.busqueda(archivo_clientes, archivo_viaticos, 4)
        elif opcion == "5":
            tipo_log = "Salir"
            funciones.escribir_log(tipo_log)
            exit();

menu()