def dia_semana(numero:int):
     """
     funcion que pasa de un numero a un dia de la semana
     """
#aprovechamos los diccionarios para darle a cada numero (clave) un valor
     dias = {
        1: "Lunes",
        2: "Martes",
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sábado",
        7: "Domingo"
    }
     return dias.get(numero, "error")

def piramide (filas):

  for i in range (filas,0,-1):
    for j in range (i,0,-1):
      print (j, end = " ")
    print ()
def compara_numeros(a,b):
  """
  funcion que compara 2 numeros
  """
  
  if a > b:
    return (f"´{a} es mayor que {b}")
    
  elif b > a:
    return (f"{b} es mayor que {a}")
    
  else:
    return (f"{a} y {b} son iguales")
    
def cuenta_letra(texto:str, letra:str):
  """
  funcion que cuenta la cantidad de apariciones de una letra en un string
  """

  mayusculas = 0
  minusculas = 0
  for i in texto:
    if letra.capitalize() == i:
      mayusculas = mayusculas + 1
    if letra.lower() == i:
      minusculas = minusculas + 1
  return (f"hay {mayusculas} mayusculas y {minusculas} minusculas")

def crea_diccio(texto:str):

  """
  funcion que de un string crea un diccionario clave(cada letra) y valor (el numero de apariciones de esa letra)

  """
  texto = texto.lower()
  dicc = {}
  for letra in texto:
    if letra in dicc:
      dicc[letra] +=1
    else:
      dicc[letra] = 1
  return dicc  #habia metido el return en el bucle y solo me salia el primer valor del diccionario

def nueva_lista(lista:list, comando:str, elemento=None):

  """
  funcion que añade o elimina de una lista un elemento dado.
  Los comandos validos son add o remove
  hay que pasarlos como string
  """
  if comando == "add":
    lista.append(elemento)
  elif comando == "remove":
    try:
      lista.remove(elemento)
    except ValueError: 
      print ("El elemento no esta en la lista")
  else:
    print("Comando incorrecto")
  return lista

def frase(*palabras):
  return " ".join(palabras)

def fibonacci(n: int):
    """
    funcion que devuelve el enésimo número de la serie de Fibonacci de forma recursiva.
    """
    if n == 0:
      return 0
    elif n == 1:
      return 1
    elif n < 0:
       return "No existe"
    else:
      return fibonacci(n-1) + fibonacci(n-2)

import math as m
def area_cuadrado(lado):
  """
  funcion area cuadrado segun su lado
  """
  area = lado * lado
  return area
def area_triangulo(base,altura):
  """
  funcion area triangulo segun base y altura
  """
  area = base * altura /2
  return area
def area_circ(radio):
  """
  funcion area circulo segun radio
  """
  area = m.pi * radio * radio
  return area

