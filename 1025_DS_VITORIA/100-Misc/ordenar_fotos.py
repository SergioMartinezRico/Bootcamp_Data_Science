from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import shutil

# ---------- CONFIGURACIÓN ----------
# Carpeta donde están tus fotos (cambia la ruta)
CARPETA_FOTOS = Path(r"C:\Users\TuUsuario\Descargas\Fotos")

# Extensiones que se van a procesar
EXTENSIONES_VALIDAS = [".jpg", ".jpeg", ".png"]

# Carpeta para fotos sin metadatos EXIF
CARPETA_SIN_FECHA = "Sin_fecha"


# ---------- FUNCIONES ----------

def obtener_fecha_exif(ruta):
    """
    Devuelve la fecha original de toma ('DateTimeOriginal') del EXIF.
    Si no existe, devuelve None.
    """
    try:
        img = Image.open(ruta)
        exif = img._getexif()
        if not exif:
            return None

        for tag, valor in exif.items():
            nombre = TAGS.get(tag)
            if nombre == "DateTimeOriginal":
                return valor  # Formato: "YYYY:MM:DD HH:MM:SS"

    except Exception:
        return None

    return None


def convertir_a_ano_mes(fecha_exif):
    """
    Convierte "YYYY:MM:DD HH:MM:SS" → "YYYY_MM"
    """
    ano, mes, *_ = fecha_exif.split()[0].split(":")
    return f"{ano}_{mes}"


def mover_archivo(origen, destino):
    """
    Mueve el archivo al destino, evitando sobrescribir si ya existe.
    """
    destino_final = destino / origen.name
    contador = 1
    while destino_final.exists():
        nuevo_nombre = f"{origen.stem}_{contador}{origen.suffix}"
        destino_final = destino / nuevo_nombre
        contador += 1

    shutil.move(str(origen), str(destino_final))
    return destino_final


def ordenar_fotos_por_fecha_captura(carpeta):
    """
    Recorre la carpeta y organiza las fotos en subcarpetas por año/mes.
    """
    sin_exif = 0
    total = 0
    carpeta = Path(carpeta)

    for archivo in carpeta.iterdir():
        if archivo.is_file() and archivo.suffix.lower() in EXTENSIONES_VALIDAS:
            total += 1
            fecha = obtener_fecha_exif(archivo)

            if not fecha:
                destino = carpeta / CARPETA_SIN_FECHA
                destino.mkdir(exist_ok=True)
                mover_archivo(archivo, destino)
                sin_exif += 1
                print(f"⚠️ {archivo.name} → Sin metadatos EXIF")
                continue

            ano_mes = convertir_a_ano_mes(fecha)
            destino = carpeta / ano_mes
            destino.mkdir(exist_ok=True)

            mover_archivo(archivo, destino)
            print(f"✅ {archivo.name} → {ano_mes}")

    # Resumen final
    print("\n----- RESUMEN -----")
    print(f"Total de fotos procesadas: {total}")
    print(f"Fotos sin EXIF: {sin_exif}")
    print(f"Fotos clasificadas: {total - sin_exif}")


# ---------- EJECUCIÓN ----------
if __name__ == "__main__":
    ordenar_fotos_por_fecha_captura(CARPETA_FOTOS)


