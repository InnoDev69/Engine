import subprocess
import shutil
import os

def compilar_y_mover(input_path, output_folder):
    try:
        # Verificar si el archivo de entrada existe
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"El archivo {input_path} no existe.")

        os.makedirs(output_folder, exist_ok=True)

        command = f'C:\\Users\\yamir\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\pyinstaller --onefile {input_path}'

        subprocess.run(command, shell=True)

        compiled_file = os.path.join("dist", os.path.basename(input_path).replace(".py", ".exe"))

        shutil.copy2(compiled_file, output_folder)

        print(f"Compilación exitosa. Archivo copiado a: {output_folder}")

    except Exception as e:
        print(f"Error durante la compilación: {e}")

script_name = input("Ingresa nombre del script:")

archivo_input = script_name
carpeta_output = "E:\\Descargas\\hwmonitor_1.51\\a\\sources"

compilar_y_mover(archivo_input, carpeta_output)
