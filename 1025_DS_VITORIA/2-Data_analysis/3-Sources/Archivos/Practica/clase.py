import os
import shutil

class Ordenar_Carpeta:

  """
  ordena los archivos segun su extension en diversas carpetas.
  """
  def __init__(self, ruta_inicio ="./ej_descargas"):
    
    self.ruta_inicio = ruta_inicio
    self.doc_types = ('.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx')
    self.img_types = ('.jpg', '.jpeg', '.png', '.svg', '.gif')
    self.software_types = ('.exe', '.py','.ipynb')
    self.carpetas = ["doc_types", "img_types", "software_types", "others"]

  def Crear_Carpeta (self):

    """
    crea carpetas desde una lista dada
    si existe la ruta no hace nada
    """

    for carpeta in self.carpetas:
      ruta = os.path.join(self.ruta_inicio, carpeta)
      os.makedirs(ruta, exist_ok=True)

  def Mover_Archivos (self):

    """
    mueve los archivos dependiendo de su extension al tipo de carpeta que le corresponde
    """

    elementos = os.listdir(self.ruta_inicio)
    for elemento in elementos:
      ruta_inicio = os.path.join(self.ruta_inicio,elemento)

      if os.path.isdir(ruta_inicio) and elemento in self.carpetas:  #si existe el archivo o la carpeta, no hace nada
        continue
# condicionales para saber las extensiones
      if elemento.endswith(self.doc_types):
        shutil.move(ruta_inicio, "./ej_descargas/doc_types")
      elif elemento.endswith(self.img_types):
        shutil.move(ruta_inicio, "./ej_descargas/img_types")
      elif elemento.endswith(self.software_types):
        shutil.move(ruta_inicio, "./ej_descargas/software_types")
      else:
        shutil.move(ruta_inicio, "./ej_descargas/others")