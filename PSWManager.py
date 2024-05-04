import string
import random
import secrets
import pyperclip
import customtkinter


def generarPasswAleatoria():
    #El algoritmo debe ser randomizar 3 espacios de caracteres 'normales', entre esos espacios cierto número de caracteres especiales y numeros
    # Generar los números aleatorios con la restricción para cómo de largos pueden ser la contraseña
    numero1 = random.randint(5, 10)
    numero2 = random.randint(0, 10 - numero1)
    numero3 = random.randint(0, 10 - numero1 - numero2)

    # Generar los numeros de restriccion para lo largo de caracteres especiales
    numero4 = random.randint(1, 5)
    numero5 = random.randint(0, 5 - numero4)

    cadena = []
    #Primer string de caracteres
    resultado1 = ''.join(secrets.choice(caracteres_permitidos1) for _ in range(numero1))
    cadena.append(resultado1)
    #primer intervalo de caracteres permitidos 2
    resultado2 = ''.join(secrets.choice(caracteres_permitidos2) for _ in range(numero4))
    cadena.append(resultado2)

    #Segundo string de caracteres
    resultado3 = ''.join(secrets.choice(caracteres_permitidos1) for _ in range(numero2))
    cadena.append(resultado3)
    #Segund intervalo de caracteres permitidos 2
    resultado4 = ''.join(secrets.choice(caracteres_permitidos2) for _ in range(numero5))
    cadena.append(resultado4)

    #Tercer string de caracteres
    resultado5 = ''.join(secrets.choice(caracteres_permitidos1) for _ in range(numero3))
    cadena.append(resultado5)

    resultadoFinal = ''.join(cadena)
    return resultadoFinal

def actualizarTxt():
    # Escribir los elementos del diccionario en el archivo de texto
    with open(nombre_archivo, 'w') as archivo:
        for pagina, contraseña in diccionario_contrasennas.items():
            archivo.write(f"{pagina}: {contraseña}\n")

    print(f"Los elementos del diccionario se han guardado en '{nombre_archivo}'.")
    pintaBotonesContrasenna()
    print("Se han vuelto a imprimir los botones actualizados")

def opcionUno():
    pagina = entry.get().strip()

    if pagina == "":
        return None

    if pagina in diccionario_contrasennas:
         return pagina

    print("Generando contraseña...")
    contraseñaGenerada = generarPasswAleatoria()

    diccionario_contrasennas[pagina] = contraseñaGenerada
    print("fContraseña {contraseñaGenerada} añadida...")

    actualizarTxt()
    entry.delete(0, customtkinter.END)
    '''Resolucion para consola
    # pagina = input("¿Para qué página/app es la contraseña? ").strip()
    # acabado = False

    # #Si ya existe la pagina/web
    # if pagina in diccionario_contrasennas:
    #     return pagina


    # while not acabado:
    #     print("Generando contraseña...")
    #     contraseñaGenerada = generarPasswAleatoria()
    #     confirmacionContraseña = input(f"La contraseña generada es: {contraseñaGenerada}, te parece bien? ").strip().lower()
        
    #     if confirmacionContraseña == "si" or confirmacionContraseña == "s":
    #         diccionario_contrasennas[pagina] = contraseñaGenerada
    #         print("Contraseña añadida...")
    #         acabado = True
    actualizarTxt()'''

def opcionDos():
    # Imprimir todas las contraseñas del diccionario
    print("--- Contraseñas guardadas ---")
    contrasennas = ""
    for clave,contrasenna in diccionario_contrasennas.items():
        contrasennas=contrasennas + (" "+clave +": " +contrasenna +"\n")
        print(f"{clave} : {contrasenna}")
    print("-----------------------------")
    #info_contrasennas.set(contrasennas)

    pintaBotonesContrasenna()


def opcionCuatro():
    respuesta = entry.get()

    if respuesta in diccionario_contrasennas:
        del diccionario_contrasennas[respuesta]
        actualizarTxt()
    entry.delete(0, customtkinter.END)

def ctkInit():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

def mostrar_info(clave):
    # Esta función copia el texto del valor de la clave en el portapapeles
    valor = diccionario_contrasennas.get(clave, "")
    pyperclip.copy(valor)
    print(f"Valor de la clave {clave} copiado al portapapeles: {valor}")

def pintaBotonesContrasenna():
    for boton in botones_contrasennas:
        boton.destroy()
    # Crear y colocar los botones
    for clave in diccionario_contrasennas.keys():
        boton = customtkinter.CTkButton(frame2, text=clave, command=lambda c=clave: mostrar_info(c))
        boton.pack(pady=5)

        botones_contrasennas.append(boton)

# Definir el diccionario con la informacion
diccionario_contrasennas = {}

# Definir los caracteres permitidos
caracteres_normales = string.ascii_letters
caracteres_especiales = string.punctuation
caracteres_numeros =  string.digits

caracteres_permitidos1 = caracteres_normales + caracteres_numeros
caracteres_permitidos2 = caracteres_especiales + caracteres_numeros

#Leer el contenido que ya existe
# Nombre del archivo de texto
nombre_archivo = "contraseñas.txt"

# Leer el contenido del archivo de texto y guardar en el diccionario
with open(nombre_archivo, 'r') as archivo:
    for linea in archivo:
        clave, valor = linea.strip().split(": ")
        diccionario_contrasennas[clave] = valor


# Create main window
ctkInit()
root = customtkinter.CTk()
root.title("Password Manager 🔒")
root.geometry("700x350")

frame = customtkinter.CTkFrame(master=root)
frame.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)

# Create buttons
opciones = ["Crear Nueva Contraseña", "Ver Contraseñas", "Eliminar Contraseña"]
botones_contrasennas = []
boton1 = customtkinter.CTkButton(frame, text= opciones[0], command=opcionUno)
boton1.pack(pady=20,fill=customtkinter.BOTH)

boton1 = customtkinter.CTkButton(frame, text= opciones[1], command=opcionDos)
boton1.pack(pady=20,fill=customtkinter.BOTH)

boton1 = customtkinter.CTkButton(frame, text= opciones[2], command=opcionCuatro)
boton1.pack(pady=20,fill=customtkinter.BOTH)

frame2 = customtkinter.CTkFrame(root)
frame2.pack(pady=20, side= customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True)

entry = customtkinter.CTkEntry(frame2, font=("Arial", 14))
entry.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH)
texto_entry = customtkinter.StringVar()

# info_contrasennas= customtkinter.StringVar()
# texto_contrasennas = customtkinter.CTkLabel(frame2, textvariable=info_contrasennas, font=("Arial", 14))
# texto_contrasennas.pack(pady=20, side=customtkinter.TOP, fill=customtkinter.BOTH)

# Run the main event loop
root.mainloop()

'''# loop = True
# while loop:
#     #Quiere meter una nueva contraseña?
#     #sí/no
#     print("---- MENÚ ----")
#     print("1. Crear nueva contraseña")
#     print("2. Ver todas las contraseñas")
#     print("3. Eliminar una web/app")
#     print("-------------")

#     answer = int(input())

#     if answer  ==  1:
#         opcionUno(diccionario_contrasennas)
#     elif answer == 2:
#         opcionDos(diccionario_contrasennas)
#     elif answer == 3:
#         opcionCuatro(diccionario_contrasennas, nombre_archivo)
#     else:
#         loop = False
'''
