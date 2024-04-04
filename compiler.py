import subprocess
import shutil
import os

def compilar_y_mover(input_path, output_folder):
    try:
        # Verificar si el archivo de entrada existe
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"El archivo {input_path} no existe.")

        # Crear la carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)

        # Comando de PyInstaller para compilar el script en un solo archivo ejecutable
        command = f'C:\\Users\\yamir\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pyinstaller --onefile {input_path}'

        # Ejecutar el comando en la terminal o símbolo del sistema
        subprocess.run(command, shell=True)

        # Obtener el nombre del archivo compilado
        compiled_file = os.path.join("dist", os.path.basename(input_path).replace(".py", ".exe"))

        # Copiar el archivo compilado a la carpeta de salida
        shutil.copy2(compiled_file, output_folder)

        print(f"Compilación exitosa. Archivo copiado a: {output_folder}")

    except Exception as e:
        print(f"Error durante la compilación: {e}")

# Reemplaza 'game.py' con el nombre real de tu script
script_name = input("Ingresa nombre del script:")

# Rutas de entrada y salida
archivo_input = script_name
carpeta_output = "E:\\Descargas\\hwmonitor_1.51\\a\\sources"

# Llamar a la función con las rutas proporcionadas
compilar_y_mover(archivo_input, carpeta_output)
