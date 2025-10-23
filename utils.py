import numpy as np
import random

#clases

#clase barco


class Barco:
    """
    Representa un barco:
    - Tiene una eslora (tamaño)
    - Guarda sus posiciones
    - Registra los impactos recibidos
    - Sabe si está hundido
    """

    def __init__(self, eslora):
        self.eslora = eslora
        self.coordenadas = []  # lista de tuplas (fila, columna)
        self.disparos = 0

    def registrar_disparo(self):
        """Suma un impacto al barco"""
        self.disparos += 1

    def hundido(self):
        """True si los impactos igualan o superan la eslora"""
        if self.disparos >= self.eslora:
            return True
        else:
            return False

#clase tablero

class Tablero:
    """
    Representa un tablero de Hundir la Flota:
    - self.tablero_juego: posiciones reales de los barcos
    - self.tablero_mostrar: lo que se va mostrando al jugador
    - self.posiciones : lista de posiciones
    - self.libre : lista de casillas que tienen que estar libres alrededor de un barco
    """

    def __init__(self, tamano=10):
        self.tamano = tamano
        self.tablero_juego = np.full((tamano, tamano), "_")   # tablero interno
        self.tablero_mostrar = np.full((tamano, tamano), "_") # tablero que se muestra
        self.posiciones = []  # lista de todos los barcos
        self.libres = set()   # celdas alrededor de barcos

    # comprobamos si un barco se puede colocar

    def puede_colocar(self, posiciones):
        for fila, col in posiciones:
            if (fila, col) in self.libres:
                return False
            if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
                return False
        return True

   #colocar un barco dandole una eslora

    def colocar_barco(self, eslora):
        colocado = False
        intentos = 0
        while colocado == False and intentos < 1000:
            intentos += 1
            barco = Barco(eslora)
            orientacion = random.choice("HV")

            if orientacion == "H":
                fila = random.randint(0, self.tamano - 1)
                col = random.randint(0, self.tamano - eslora)
                posiciones = [(fila, col + i) for i in range(eslora)]
            else:
                fila = random.randint(0, self.tamano - eslora)
                col = random.randint(0, self.tamano - 1)
                posiciones = [(fila + i, col) for i in range(eslora)]

            if self.puede_colocar(posiciones):
                barco.coordenadas = posiciones
                self.posiciones.append(barco)
                for f, c in posiciones:
                    self.tablero_juego[f, c] = "B"
                    # marcar alrededor como libre
                    for i in range(f-1, f+2):
                        for j in range(c-1, c+2):
                            if 0 <= i < self.tamano and 0 <= j < self.tamano:
                                self.libres.add((i, j))
                colocado = True

    #repite colocar con una lista de valores
    def colocar_flota(self, flota):
        for eslora in flota:
            self.colocar_barco(eslora)

   #disparar

    def disparar(self, fila, col):
        if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
            return "fuera"

        if self.tablero_mostrar[fila, col] != "_":
            return "repetido"

        if self.tablero_juego[fila, col] == "B":
            self.tablero_mostrar[fila, col] = "X"
            for barco in self.posiciones:
                if (fila, col) in barco.coordenadas:
                    barco.registrar_disparo()
                    if barco.hundido == True:
                        print("y hundido!!!")
                    break
            return "tocado"
        else:
            self.tablero_mostrar[fila, col] = "O"
            return "agua"

   # comprobamos si todos estan hundidos

    def todos_hundidos(self):
        for barco in self.posiciones:
            if barco.hundido() == False:
                return False
        return True

  # mostrar tablero

    def mostrar(self):

        tablero = self.tablero_mostrar.copy().astype(str)
        # Columna de números 
        col_numeros = np.array([[" 1"], [" 2"], [" 3"], [" 4"], [" 5"],[" 6"], [" 7"], [" 8"], [" 9"], ["10"]])
        # Fila de letras mas un hueco para cuadrar
        fila_letras = np.array([["  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]])
        # Concatenar números a la izquierda
        tablero_numerado = np.hstack((col_numeros, tablero))
        # Concatenar letras arriba
        tablero_final = np.vstack((fila_letras, tablero_numerado))
        print(tablero_final)

