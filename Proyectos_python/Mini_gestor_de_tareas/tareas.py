#actividad trabajo integrador evaluativo
#modulos de funciones tareas


tareas = []

def agregar():
    nombre = input("nombre de la tarea: ")
    fecha = input("fecha de vencimiento(DD/MM/AAAA): ")
    tareas.append([nombre,fecha])

def mostrar():
    if not tareas:
        print("no hay tareas pendientes")
        return
    for i in range(len(tareas)):
        tarea = tareas[i]
        print(str(i + 1) + "_" + tarea[0] + "_" + tarea[1])
    

def completar():
    mostrar()
    if tareas:
        yair1 = int(input("numero de tarea que quiere marcar como completada: "))
        tareas.pop(yair1-1)

def editar():
    mostrar()
    if tareas:
        yair2 = int(input("numero de tarea que quiera editar: "))
        nombre = (input("nuevo nombre: "))
        fecha = (input("nueva fecha: "))
        tareas[yair2-1] = [nombre, fecha]