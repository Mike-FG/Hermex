import string
import random
import secrets
import pyperclip
import customtkinter
from tkinter import messagebox
import os
from cryptography.fernet import Fernet # Para encriptación del archivo

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
    with open(nombre_archivo, 'w') as archivo:
        for clave, valor in diccionario_contrasennas.items():
            linea_cifrada = cipher_suite.encrypt(f"{clave}:{valor}".encode()).decode()
            archivo.write(f"{linea_cifrada}\n")
        # Escribir los elementos del diccionario en el archivo de texto
        # with open(nombre_archivo, 'w') as archivo:
        #     for pagina, contraseña in diccionario_contrasennas.items():
        #         archivo.write(f"{pagina}: {contraseña}\n")

    ##print(f"Los elementos del diccionario se han guardado en '{nombre_archivo}'.")

def opcionUno():
    pagina = entry.get().strip()

    if pagina == "":
        return None

    if pagina in diccionario_contrasennas:
         return pagina

    #print("Generando contraseña...")
    contraseñaGenerada = generarPasswAleatoria()

    diccionario_contrasennas[pagina] = contraseñaGenerada
    #print("fContraseña {contraseñaGenerada} añadida...")

    actualizarTxt()
    pintaBotonesContrasenna()
    entry.delete(0, customtkinter.END)



def opcionDos():
    respuesta = entry.get()

    if respuesta in diccionario_contrasennas:
        del diccionario_contrasennas[respuesta]
        actualizarTxt()
        pintaBotonesContrasenna()
    entry.delete(0, customtkinter.END)

def opcionTres():
    respuesta = entry.get()
    
    try:
        clave, valor = respuesta.split(":")
        clave = clave.strip()
        valor = valor.strip()

        diccionario_contrasennas[clave] = valor
        actualizarTxt()
        pintaBotonesContrasenna()
        entry.delete(0, customtkinter.END)

    except(TypeError, ValueError) as e:
        print("Input no válido para crear contraseña personalizada", e)

def ctkInit():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

def mostrar_info(clave):
    # Esta función copia el texto del valor de la clave en el portapapeles
    valor = diccionario_contrasennas.get(clave, "")
    pyperclip.copy(valor)
    #print(f"Valor de la clave {clave} copiado al portapapeles: {valor}")

def pintaBotonesContrasenna():
    for boton in botones_contrasennas:
        boton.destroy()
    # Crear y colocar los botones
    for clave in diccionario_contrasennas.keys():
        boton = customtkinter.CTkButton(frame3, text=clave, fg_color="#0E46A3",command=lambda c=clave: mostrar_info(c))
        boton.pack(pady=5)
        
        botones_contrasennas.append(boton)

def login():
    login_password = password_entry.get()

    if hermex_contrasenna == login_password:
        # messagebox.showinfo("Login", "Inicio de sesión exitoso")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showinfo("Login", "Contraseña incorrecta")

def open_login_window():
    # Create Login window
    global login_window
    login_window = customtkinter.CTk()
    login_window.wm_iconbitmap("Hermex_logo.ico")
    login_window.title("Hermex")
    login_window.geometry("300x200")

    customtkinter.CTkLabel(login_window, text="Introduce la contraseña para iniciar sesión\n o para renovar la contraseña").pack()
    global password_entry
    password_entry = customtkinter.CTkEntry(login_window, show="*")
    password_entry.pack(pady=20)

    login_button = customtkinter.CTkButton(login_window, text="Iniciar Sesión", fg_color="#0E46A3", command=login)
    login_button.pack(pady= 5)

    login_button2 = customtkinter.CTkButton(login_window, text="Cambiar contraseña", fg_color="#0E46A3", command=register_validation)
    login_button2.pack(pady= 5)

    # Run the main event loop
    login_window.mainloop()

def register_validation():

    if password_entry.get() == hermex_contrasenna:
        login_window.destroy()
        open_register_window()
    else:
         messagebox.showinfo("Advertencia", "Introduce la contraseña actual")

def creaContrasennaHermex():
    with open(hermex_archivo, "w") as archivo:
        global hermex_contrasenna
        hermex_contrasenna = register_entry.get()
        hermex_contrasenna_cifrada = cipher_suite.encrypt(f"{hermex_contrasenna}".encode()).decode()
        archivo.write(f"{hermex_contrasenna_cifrada}\n")   
    
    register_window.destroy()
    open_login_window()

def open_main_window():
    # Create main window
    root = customtkinter.CTk()
    root.wm_iconbitmap("Hermex_logo.ico")
    root.title("Hermex")
    root.geometry("700x350")

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(side=customtkinter.LEFT, fill=customtkinter.BOTH, expand=True)

    # Create buttons
    opciones = ["Crear nueva contraseña", "Ver contraseñas", "Eliminar contraseña", "Añadir contraseña personalizada"]
    global botones_contrasennas
    botones_contrasennas = []

    boton1 = customtkinter.CTkButton(frame, text= opciones[0], fg_color="#0E46A3", command=opcionUno)
    boton1.pack(pady=20,fill=customtkinter.BOTH)

    # boton1 = customtkinter.CTkButton(frame, text= opciones[1], command=opcionDos)
    # boton1.pack(pady=20,fill=customtkinter.BOTH)

    boton1 = customtkinter.CTkButton(frame, text= opciones[2], fg_color="#0E46A3", command=opcionDos)
    boton1.pack(pady=20,fill=customtkinter.BOTH)

    boton1 = customtkinter.CTkButton(frame, text= opciones[3], fg_color="#0E46A3", command=opcionTres)
    boton1.pack(pady=20,fill=customtkinter.BOTH)

    texto_info = customtkinter.CTkLabel(frame, text="Formato válido-> 'Aplicación : ContraseñaPersonalizada'")
    texto_info.pack(fill=customtkinter.BOTH)

    frame2 = customtkinter.CTkFrame(root)
    frame2.pack(side= customtkinter.RIGHT, fill=customtkinter.BOTH, expand=True)

    global frame3
    frame3 = customtkinter.CTkScrollableFrame(frame2)
    frame3.pack(side= customtkinter.TOP, fill=customtkinter.BOTH, expand=True)

    # frame_input_feedback = customtkinter.CTkFrame(frame2)
    # frame_input_feedback.pack(side=customtkinter.BOTTOM,fill=customtkinter.BOTH, expand=True)

    
    # feedback = customtkinter.CTkTextbox(frame_input_feedback, font=("Arial", 14), width= 350, height=10)
    # feedback.pack(side= customtkinter.TOP)

    global entry
    entry = customtkinter.CTkEntry(frame2, font=("Arial", 14))
    entry.pack(side=customtkinter.BOTTOM, fill=customtkinter.BOTH)

    pintaBotonesContrasenna()
    # texto_entry = customtkinter.StringVar()

    root.mainloop()

def open_register_window():
    # Create Register window
    global register_window
    register_window = customtkinter.CTk()
    register_window.wm_iconbitmap("Hermex_logo.ico")
    register_window.title("Hermex")
    register_window.geometry("300x200")

    customtkinter.CTkLabel(register_window, text="Introduce una contraseña maestra\n para acceder a Hermex:").pack()
    global register_entry
    register_entry = customtkinter.CTkEntry(register_window)
    register_entry.pack(pady=20)

    register_button = customtkinter.CTkButton(register_window, text="Crear cuenta", fg_color="#0E46A3", command=creaContrasennaHermex)
    register_button.pack()

    register_window.mainloop()
    
# Definir el diccionario con la informacion
diccionario_contrasennas = {}

# Definir los caracteres permitidos
caracteres_normales = string.ascii_letters
caracteres_especiales = string.punctuation
caracteres_numeros =  string.digits

# Eliminamos ':' de los posibles
caracteres_especiales.replace(':', '')

# Creamos los grupos de caracteres permitidos
caracteres_permitidos1 = caracteres_normales + caracteres_numeros
caracteres_permitidos2 = caracteres_especiales + caracteres_numeros

# Leer el contenido que ya existe
# Nombre del archivo de texto
nombre_archivo = "contraseñas.txt"
clave_archivo = "config.bin"
hermex_archivo= "config.txt"
# Definimos nombres de las variables de la clave
cipher_key = None
cipher_suite = None

ctkInit()

# Conseguimos la clave o la generamos si no existe el archivo
if not os.path.exists(clave_archivo):
    cipher_key = Fernet.generate_key()
    with open(clave_archivo, "wb") as archivoClave:
        archivoClave.write(cipher_key)
else:
    with open(clave_archivo, "rb") as archivoClave:
        cipher_key = archivoClave.read()

cipher_suite = Fernet(cipher_key)

# Leer el contenido del archivo de texto y guardar en el diccionario
if os.path.exists(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        if os.path.getsize(nombre_archivo) > 0:
            lineas_texto = archivo.readlines()

            for linea_cifrada in lineas_texto:
                linea_descifrada = cipher_suite.decrypt(linea_cifrada.encode()).decode()    

                app, contrasenna = linea_descifrada.split(":")
                diccionario_contrasennas[app] = contrasenna
else:
    with open(nombre_archivo, "w") as archivo:
        archivo.close()

if os.path.exists(hermex_archivo):
    with open(hermex_archivo, "r") as archivo:
        global hermex_contrasenna
        hermex_contrasenna_cifrada = archivo.readline()
        hermex_contrasenna = cipher_suite.decrypt(hermex_contrasenna_cifrada.encode()).decode()
    
    open_login_window()
else:
    open_register_window()


'''# loop = True
# while loop:
#     #Quiere meter una nueva contraseña?
#     #sí/no
#     #print("---- MENÚ ----")
#     #print("1. Crear nueva contraseña")
#     #print("2. Ver todas las contraseñas")
#     #print("3. Eliminar una web/app")
#     #print("-------------")

#     answer = int(input())

#     if answer  ==  1:
#         opcionUno(diccionario_contrasennas)
#     elif answer == 2:
#         opcionDos(diccionario_contrasennas)
#     elif answer == 3:
#         opcionDos(diccionario_contrasennas, nombre_archivo)
#     else:
#         loop = False
'''
