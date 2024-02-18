import psutil
import time
import keyboard
import os
import socket
import subprocess
import requests

def check_process_running(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

program_name = "java.exe"  # Nombre del programa (Java.exe es el archivo ejecutado por los servidores de minecraft) 

while not keyboard.is_pressed("esc"):
    if check_process_running(program_name):
        print(f"El servidor se esta ejecutando")
    else:
        print(f"El servidor esta esperdando una conexión")
        def main():
            # Definir el host y el puerto que deseas monitorear
            host = ''  # El host vacío indica que escucharemos en todas las interfaces de red
            puerto = 25565  # Puerto que deseas monitorear (Pueto por defecto para servidores de minecraft)

            # Crear un socket TCP/IP
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Enlace del socket a la dirección y puerto especificados
            servidor.bind((host, puerto))

            # Escuchar conexiones entrantes
            servidor.listen(1)

            print(f"Escuchando en el puerto {puerto}...")

            # Ruta al directorio donde se encuentra el archivo .bat
            ruta_bat = "C:\\Users\\luuca\\OneDrive\\Documentos\\Server\\Start.bat"

            while not keyboard.is_pressed("esc"):
                # Esperar una conexión
                conexion, direccion = servidor.accept()

                # Usa una api para comprobar la ubicacion desde donde proviene la ip
                response = requests.get(f"https://api.ip2location.io/?key=69BE6A0506F38CF849E5326F67DE9756&ip={direccion[0]}&format=json")
                if response.status_code == 200:
                    response_json = response.json()

                # Comprueba que la ip sea proveniente de Uruguay para abrir el servidor
                if response_json["country_name"] == "Uruguay":
                    try:
                        print(f"Conexión entrante de: {direccion[0]}:{direccion[1]}")
                        # Cuando se detecta una conexión, ejecutar el archivo .bat
                        subprocess.Popen([ruta_bat], cwd=os.path.dirname(ruta_bat))

                    except Exception as e:
                        print("Error al ejecutar el archivo .bat:", e)
                    finally:
                        # Cerrar la conexión
                        conexion.close()

                    if check_process_running(program_name):
                        # Aquí puedes colocar código para verificar la salida del servidor
                        # Por ejemplo, podrías leer el archivo de registro del servidor o interactuar con él de alguna manera

                        # Por ahora, enviaré el comando /list cada 5 minutos para demostrar cómo se enviarían comandos
                        # Debes reemplazar esto con la lógica adecuada para verificar la salida del servidor
                        subprocess.run(['cmd', '/c', 'echo /list | nc localhost 25565'], shell=True)

        if __name__ == "__main__":
            main()
       
    #Espera 5 minutos antes de volver a comenzar el loop de comprobación del puerto 
    time.sleep(300)


