#actividad trabajo integrador evaluativo
#taraea principal
import tareas

def principal():
    while True:
        print("\n__._.__MENU__._.__")
        print("1: agregar tarea")
        print("2: completar tarea")
        print("3: editar tarea")
        print("4: mostrar tareas pendientes")
        print("5: salir")
        opcion = input("ingrese el numero de la opcion que desea realizar: ")

        if opcion == "1":
            tareas.agregar()
        elif opcion == "2":
            tareas.completar()
        elif opcion == "3":
            tareas.editar()
        elif opcion == "4":
            tareas.mostrar()
        elif opcion == "5":
            print("bye bye bye")
            break
        else:
            print("opcion invalida,intente otra cosa")

principal()