from clase import Ordenar_Carpeta


if __name__ == "__main__":
    # Puedes cambiar la ruta si quieres
    ruta = "./ej_descargas"
    organizador = Ordenar_Carpeta(ruta)

    organizador.Crear_Carpeta()
    organizador.Mover_Archivos()

    print("✅ Archivos ordenados correctamente.")


