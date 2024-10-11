import csv
import pandas as pd
from datetime import datetime, timedelta
import re
from statistics import mode, StatisticsError

unidades = []
clientes = []
prestamos = []

def cargar_datos():
    global unidades, clientes, prestamos
    try:
        with open('unidades.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                unidades.append({'clave': int(row[0]), 'rodada': int(row[1]), 'color': row[2]})
    except FileNotFoundError:
        print("No se encontró el archivo de unidades.")
        
    try:
        with open('clientes.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                clientes.append({'clave': int(row[0]), 'apellidos': row[1], 'nombres': row[2], 'telefono': row[3]})
    except FileNotFoundError:
        print("No se encontró el archivo de clientes.")
        
    try:
        with open('prestamos.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                prestamos.append({
                    'folio': int(row[0]),
                    'clave_unidad': int(row[1]),
                    'clave_cliente': int(row[2]),
                    'fecha_prestamo': datetime.strptime(row[3], '%m-%d-%Y'),
                    'cantidad_dias': int(row[4]),
                    'fecha_retorno': datetime.strptime(row[5], '%m-%d-%Y') if row[5] else None
                })
    except FileNotFoundError:
        print("No se encontró el archivo de préstamos.")

def guardar_datos():
    with open('unidades.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for unidad in unidades:
            writer.writerow([unidad['clave'], unidad['rodada'], unidad['color']])
    
    with open('clientes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for cliente in clientes:
            writer.writerow([cliente['clave'], cliente['apellidos'], cliente['nombres'], cliente['telefono']])
    
    with open('prestamos.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for prestamo in prestamos:
            writer.writerow([
                prestamo['folio'], 
                prestamo['clave_unidad'], 
                prestamo['clave_cliente'], 
                prestamo['fecha_prestamo'].strftime('%m-%d-%Y'), 
                prestamo['cantidad_dias'], 
                prestamo['fecha_retorno'].strftime('%m-%d-%Y') if prestamo['fecha_retorno'] else ''
            ])

def exportar_reporte(df):
    opcion = input("¿Desea exportar este reporte? (s/n): ").strip().lower()
    if opcion == 's':
        while True:
            formato = input("Seleccione el formato de exportación (csv/excel): ").strip().lower()
            if formato in ['csv', 'excel']:
                nombre_archivo = input("Ingrese el nombre del archivo (sin extensión): ").strip()
                try:
                    if formato == 'csv':
                        df.to_csv(f"{nombre_archivo}.csv", index=False)
                        print(f"Reporte exportado como {nombre_archivo}.csv")
                    else:
                        df.to_excel(f"{nombre_archivo}.xlsx", index=False)
                        print(f"Reporte exportado como {nombre_archivo}.xlsx")
                    break
                except Exception as e:
                    print(f"Error al exportar: {e}")
            else:
                print("Formato no válido. Elija 'csv' o 'excel'.")

def submenu_listados():
    while True:
        print("\nSubmenú de Listados")
        print("1. Listado completo")
        print("2. Listar por rodada")
        print("3. Listar por color")
        print("4. Volver al Submenú de Reportes")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            listar_unidades()
        elif opcion == '2':
            listar_por_rodada()
        elif opcion == '3':
            listar_por_color()
        elif opcion == '4':
            break
        else:
            print("Opción no válida.")

def submenu_registros():
    while True:
        print("\nSubmenú de Registros")
        print("1. Registrar Unidad")
        print("2. Registrar Cliente")
        print("3. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_unidad()
        elif opcion == '2':
            registrar_cliente()
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")

def submenu_reportes():
    while True:
        print("\nSubmenú de Reportes")
        print("1. Listados")
        print("2. Reporte de Clientes")
        print("3. Reporte de Retrasos")
        print("4. Préstamos por Retornar")
        print("5. Préstamos por Periodo")
        print("6. Análisis de Datos")
        print("7. Volver al Submenú de Operaciones Avanzadas")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            submenu_listados()
        elif opcion == '2':
            listar_clientes()
        elif opcion == '3':
            generar_reporte_retrasos()
        elif opcion == '4':
            generar_prestamos_por_retornar()
        elif opcion == '5':
            prestamos_por_periodo()
        elif opcion == '6':
            analisis_datos()
        elif opcion == '7':
            break
        else:
            print("Opción no válida.")

def submenu_analisis_datos():
    while True:
        print("\nSubmenú de Análisis de Datos")
        print("1. Análisis de Datos")
        print("2. Volver al Submenú de Operaciones Avanzadas")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            analisis_datos()
        elif opcion == '2':
            break
        else:
            print("Opción no válida.")

def submenu_operaciones_avanzadas():
    while True:
        print("\nSubmenú de Operaciones Avanzadas")
        print("1. Reportes")
        print("2. Análisis de Datos")
        print("3. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            submenu_reportes()
        elif opcion == '2':
            submenu_analisis_datos()
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")

def registrar_unidad():
    try:
        clave = int(input("Ingrese la clave de la unidad: "))
        if any(u['clave'] == clave for u in unidades):
            print("Error: La clave ya existe.")
            return
        rodada = int(input("Ingrese la rodada (20, 26, 29): "))
        if rodada not in [20, 26, 29]:
            print("Error: Rodada inválida.")
            return
        color = input("Ingrese el color de la bicicleta: ").strip()
        if not color.isalpha():
            print("Error: El color solo debe contener letras.")
            return
        if not color:
            print("Error: El color no puede estar vacío.")
            return
        unidades.append({'clave': clave, 'rodada': rodada, 'color': color.capitalize()})
        print("Unidad registrada exitosamente.")
    except ValueError:
        print("Error: Entrada inválida. Asegúrese de ingresar números donde corresponda.")

def registrar_cliente():
    try:
        clave = int(input("Ingrese la clave del cliente: "))
        if any(c['clave'] == clave for c in clientes):
            print("Error: La clave ya existe.")
            return
        apellidos = input("Ingrese los apellidos del cliente: ").strip()
        if not apellidos.replace(' ', '').isalpha():
            print("Error: Los apellidos solo deben contener letras.")
            return
        nombres = input("Ingrese los nombres del cliente: ").strip()
        if not nombres.replace(' ', '').isalpha():
            print("Error: Los nombres solo deben contener letras.")
            return
        telefono = input("Ingrese el teléfono del cliente: ").strip()
        if not re.match(r'^\+?\d{7,15}$', telefono):
            print("Error: Formato de teléfono inválido.")
            return
        clientes.append({'clave': clave, 'apellidos': apellidos.capitalize(), 'nombres': nombres.capitalize(), 'telefono': telefono})
        print("Cliente registrado exitosamente.")
    except ValueError:
        print("Error: Entrada inválida. Asegúrese de ingresar números donde corresponda.")

def registrar_prestamo():
    try:
        folio = int(input("Ingrese el folio del préstamo: "))
        if any(p['folio'] == folio for p in prestamos):
            print("Error: El folio ya existe.")
            return

        listar_unidades()
        listar_clientes()

        clave_unidad = int(input("Ingrese la clave de la unidad a prestar: "))
        if not any(u['clave'] == clave_unidad for u in unidades):
            print("Error: La clave de unidad no existe.")
            return

        clave_cliente = int(input("Ingrese la clave del cliente: "))
        if not any(c['clave'] == clave_cliente for c in clientes):
            print("Error: La clave del cliente no existe.")
            return

        fecha_prestamo_str = input("Ingrese la fecha de préstamo (mm-dd-aaaa) [Presione Enter para usar la fecha actual]: ").strip()
        if fecha_prestamo_str == '':
            fecha_prestamo = datetime.now()
            print(f"Fecha de préstamo establecida a la fecha actual: {fecha_prestamo.strftime('%m-%d-%Y')}")
        else:
            fecha_prestamo = datetime.strptime(fecha_prestamo_str, '%m-%d-%Y')

        cantidad_dias_input = input("Ingrese la cantidad de días del préstamo: ").strip()
        if cantidad_dias_input == '':
            print("Error: La cantidad de días es obligatoria.")
            return
        cantidad_dias = int(cantidad_dias_input)
        if cantidad_dias <= 0:
            print("Error: La cantidad de días debe ser positiva.")
            return

        fecha_retorno = None 
        prestamos.append({
            'folio': folio,
            'clave_unidad': clave_unidad,
            'clave_cliente': clave_cliente,
            'fecha_prestamo': fecha_prestamo,
            'cantidad_dias': cantidad_dias,
            'fecha_retorno': fecha_retorno
        })
        print("Préstamo registrado exitosamente.")
    except ValueError as ve:
        print(f"Error: Entrada inválida. Asegúrese de ingresar datos en el formato correcto. Detalle: {ve}")

def registrar_retorno():
    try:
        folio = int(input("Ingrese el folio del préstamo a retornar: "))
        prestamo = next((p for p in prestamos if p['folio'] == folio), None)
        if not prestamo:
            print("Error: No se encontró un préstamo con ese folio.")
            return
        if prestamo['fecha_retorno']:
            print("Error: Este préstamo ya ha sido retornado.")
            return
        
        cliente = next((c for c in clientes if c['clave'] == prestamo['clave_cliente']), None)
        unidad = next((u for u in unidades if u['clave'] == prestamo['clave_unidad']), None)
        if cliente and unidad:
            print("\nDetalles del Préstamo a Retornar:")
            print(f"Folio: {prestamo['folio']}")
            print(f"Cliente: {cliente['nombres']} {cliente['apellidos']}")
            print(f"Unidad: {unidad['clave']} - Rodada: {unidad['rodada']} - Color: {unidad['color']}")
            print(f"Fecha de Préstamo: {prestamo['fecha_prestamo'].strftime('%m-%d-%Y')}")
            print(f"Días de Préstamo: {prestamo['cantidad_dias']}")
        else:
            print("Error: Datos del préstamo incompletos.")
            return

        fecha_retorno_str = input("Ingrese la fecha de retorno (mm-dd-aaaa): ").strip()
        fecha_retorno = datetime.strptime(fecha_retorno_str, '%m-%d-%Y')
        if fecha_retorno < prestamo['fecha_prestamo']:
            print("Error: La fecha de retorno no puede ser anterior a la fecha de préstamo.")
            return
        prestamo['fecha_retorno'] = fecha_retorno
        print("Retorno registrado exitosamente.")
    except ValueError as ve:
        print(f"Error: Entrada inválida. Asegúrese de ingresar datos en el formato correcto. Detalle: {ve}")

def listar_unidades():
    if not unidades:
        print("\nNo hay unidades registradas.")
        return
    data = [{'Clave': u['clave'], 'Rodada': u['rodada'], 'Color': u['color']} for u in unidades]
    df = pd.DataFrame(data)
    print("\nListado de Unidades:")
    print(df.to_string(index=False))
    exportar_reporte(df)

def listar_por_rodada():
    try:
        rodada = int(input("Ingrese la rodada (20, 26, 29): "))
        if rodada not in [20, 26, 29]:
            print("Error: Rodada inválida.")
            return
        filtradas = [u for u in unidades if u['rodada'] == rodada]
        if not filtradas:
            print(f"\nNo hay unidades con rodada {rodada}.")
            return
        data = [{'Clave': u['clave'], 'Rodada': u['rodada'], 'Color': u['color']} for u in filtradas]
        df = pd.DataFrame(data)
        print(f"\nUnidades con rodada {rodada}:")
        print(df.to_string(index=False))
        exportar_reporte(df)
    except ValueError:
        print("Error: Rodada inválida.")

def listar_por_color():
    color = input("Ingrese el color: ").strip()
    if not color.isalpha():
        print("Error: El color solo debe contener letras.")
        return
    filtradas = [u for u in unidades if u['color'].lower() == color.lower()]
    if not filtradas:
        print(f"\nNo hay unidades de color {color.capitalize()}.")
        return
    data = [{'Clave': u['clave'], 'Rodada': u['rodada'], 'Color': u['color']} for u in filtradas]
    df = pd.DataFrame(data)
    print(f"\nUnidades de color {color.capitalize()}:")
    print(df.to_string(index=False))
    exportar_reporte(df)

def listar_clientes():
    if not clientes:
        print("\nNo hay clientes registrados.")
        return
    data = [{'Clave': c['clave'], 'Apellidos': c['apellidos'], 'Nombres': c['nombres'], 'Teléfono': c['telefono']} for c in clientes]
    df = pd.DataFrame(data)
    print("\nListado de Clientes:")
    print(df.to_string(index=False))
    exportar_reporte(df)

def generar_reporte_retrasos():
    print("\nReporte de Retrasos:")
    data = []
    hoy = datetime.now()
    retrasos = [p for p in prestamos if p['fecha_retorno'] and p['fecha_retorno'] < hoy]
    if not retrasos:
        print("No hay retrasos en los préstamos.")
        return
    for prestamo in retrasos:
        cliente = next((c for c in clientes if c['clave'] == prestamo['clave_cliente']), None)
        unidad = next((u for u in unidades if u['clave'] == prestamo['clave_unidad']), None)
        if cliente and unidad:
            data.append({
                'Folio': prestamo['folio'],
                'Cliente': f"{cliente['nombres']} {cliente['apellidos']}",
                'Unidad': prestamo['clave_unidad'],
                'Fecha Retorno': prestamo['fecha_retorno'].strftime('%m-%d-%Y')
            })
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    exportar_reporte(df)

def generar_prestamos_por_retornar():
    print("\nPréstamos por Retornar:")
    data = []
    pendientes = [p for p in prestamos if not p['fecha_retorno']]
    if not pendientes:
        print("No hay préstamos pendientes de retorno.")
        return
    for prestamo in pendientes:
        cliente = next((c for c in clientes if c['clave'] == prestamo['clave_cliente']), None)
        unidad = next((u for u in unidades if u['clave'] == prestamo['clave_unidad']), None)
        if cliente and unidad:
            data.append({
                'Folio': prestamo['folio'],
                'Cliente': f"{cliente['nombres']} {cliente['apellidos']}",
                'Unidad': prestamo['clave_unidad'],
                'Fecha Préstamo': prestamo['fecha_prestamo'].strftime('%m-%d-%Y'),
                'Días': prestamo['cantidad_dias']
            })
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    exportar_reporte(df)

def prestamos_por_periodo():
    try:
        fecha_inicio = datetime.strptime(input("Ingrese la fecha de inicio (mm-dd-aaaa): "), '%m-%d-%Y')
        fecha_fin = datetime.strptime(input("Ingrese la fecha de fin (mm-dd-aaaa): "), '%m-%d-%Y')
        if fecha_fin < fecha_inicio:
            print("Error: La fecha de fin no puede ser anterior a la fecha de inicio.")
            return
        filtrados = [p for p in prestamos if fecha_inicio <= p['fecha_prestamo'] <= fecha_fin]
        if not filtrados:
            print(f"\nNo hay préstamos entre {fecha_inicio.strftime('%m-%d-%Y')} y {fecha_fin.strftime('%m-%d-%Y')}.")
            return
        data = []
        for prestamo in filtrados:
            cliente = next((c for c in clientes if c['clave'] == prestamo['clave_cliente']), None)
            if cliente:
                data.append({
                    'Folio': prestamo['folio'],
                    'Clave Unidad': prestamo['clave_unidad'],
                    'Fecha Préstamo': prestamo['fecha_prestamo'].strftime('%m-%d-%Y'),
                    'Cliente': f"{cliente['nombres']} {cliente['apellidos']}"
                })
        df = pd.DataFrame(data)
        print(f"\nPréstamos del {fecha_inicio.strftime('%m-%d-%Y')} al {fecha_fin.strftime('%m-%d-%Y')}:")
        print(df.to_string(index=False))
        exportar_reporte(df)
    except ValueError:
        print("Error: Formato de fecha incorrecto.")

def analisis_datos():
    print("\nAnálisis de Datos")
    
    print("\nDuración de los Préstamos:")
    if prestamos:
        dias_prestamos = [p['cantidad_dias'] for p in prestamos]
        media = pd.Series(dias_prestamos).mean()
        mediana = pd.Series(dias_prestamos).median()
        try:
            moda_val = mode(dias_prestamos)
        except StatisticsError:
            moda_val = "No hay moda única"
        minimo = pd.Series(dias_prestamos).min()
        maximo = pd.Series(dias_prestamos).max()
        desviacion = pd.Series(dias_prestamos).std()
        cuartiles = pd.Series(dias_prestamos).quantile([0.25, 0.5, 0.75]).to_dict()
        
        duracion_data = {
            'Media': [media],
            'Mediana': [mediana],
            'Moda': [moda_val],
            'Mínimo': [minimo],
            'Máximo': [maximo],
            'Desviación Estándar': [desviacion],
            'Cuartil 25%': [cuartiles.get(0.25, None)],
            'Cuartil 50%': [cuartiles.get(0.5, None)],
            'Cuartil 75%': [cuartiles.get(0.75, None)]
        }
        df_duracion = pd.DataFrame(duracion_data)
        print(df_duracion.to_string(index=False))
        exportar_reporte(df_duracion)
    else:
        print("No hay préstamos registrados para analizar duración.")
    
    print("\nRanking de Clientes:")
    ranking = {}
    for prestamo in prestamos:
        cliente = prestamo['clave_cliente']
        ranking[cliente] = ranking.get(cliente, 0) + 1
    if ranking:
        data = []
        ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        for clave, count in ranking_ordenado:
            cliente = next((c for c in clientes if c['clave'] == clave), None)
            if cliente:
                data.append({
                    'Clave': cliente['clave'],
                    'Nombre Completo': f"{cliente['nombres']} {cliente['apellidos']}",
                    'Teléfono': cliente['telefono'],
                    'Cantidad de Préstamos': count
                })
        df_ranking = pd.DataFrame(data)
        print(df_ranking.to_string(index=False))
        exportar_reporte(df_ranking)
    else:
        print("No hay préstamos registrados para generar el ranking de clientes.")
    
    print("\nPreferencias de Rentas por Rodada:")
    preferencias_rodada = {}
    for prestamo in prestamos:
        unidad = next((u for u in unidades if u['clave'] == prestamo['clave_unidad']), None)
        if unidad:
            preferencias_rodada[unidad['rodada']] = preferencias_rodada.get(unidad['rodada'], 0) + 1
    if preferencias_rodada:
        data = [{'Rodada': rodada, 'Cantidad de Préstamos': count} for rodada, count in preferencias_rodada.items()]
        df_preferencias_rodada = pd.DataFrame(data)
        df_preferencias_rodada = df_preferencias_rodada.sort_values(by='Cantidad de Préstamos', ascending=False)
        print(df_preferencias_rodada.to_string(index=False))
        exportar_reporte(df_preferencias_rodada)
    else:
        print("No hay préstamos registrados para analizar preferencias por rodada.")
    
    print("\nPreferencias de Rentas por Color:")
    preferencias_color = {}
    for prestamo in prestamos:
        unidad = next((u for u in unidades if u['clave'] == prestamo['clave_unidad']), None)
        if unidad:
            color = unidad['color'].lower()
            preferencias_color[color] = preferencias_color.get(color, 0) + 1
    if preferencias_color:
        data = [{'Color': color.capitalize(), 'Cantidad de Préstamos': count} for color, count in preferencias_color.items()]
        df_preferencias_color = pd.DataFrame(data)
        df_preferencias_color = df_preferencias_color.sort_values(by='Cantidad de Préstamos', ascending=False)
        print(df_preferencias_color.to_string(index=False))
        exportar_reporte(df_preferencias_color)
    else:
        print("No hay préstamos registrados para analizar preferencias por color.")

def menu_principal():
    cargar_datos()
    while True:
        print("\nMenú Principal")
        print("1. Registros")
        print("2. Registrar Préstamo")
        print("3. Registrar Retorno")
        print("4. Operaciones Avanzadas")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            submenu_registros()
        elif opcion == '2':
            registrar_prestamo()
        elif opcion == '3':
            registrar_retorno()
        elif opcion == '4':
            submenu_operaciones_avanzadas()
        elif opcion == '5':
            confirmacion = input("¿Está seguro que desea salir? (s/n): ").strip().lower()
            if confirmacion == 's':
                guardar_datos()
                print("Datos guardados. Saliendo del sistema.")
                break
            else:
                print("Cancelando salida.")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_principal()