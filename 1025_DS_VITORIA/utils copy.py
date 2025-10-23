import numpy as np
import random

#CLASE BARCO

class Barco:
    """
    Representa un barco:
    - Tiene una eslora (tamaño)
    - Guarda sus posiciones
    - Genera las coordenadas de su barco
    """

    def __init__(self, eslora):
        self.eslora = eslora
        self.coordenadas = []   # lista de tuplas (fila, columna)

    def generar_coordenadas(self, tamano):
        """Genera posiciones aleatorias según orientación"""
        orientacion = random.choice("HV")

        if orientacion == "H":
            fila = random.randint(0, tamano - 1)
            col = random.randint(0, tamano - self.eslora)
            posiciones = [(fila, col + i) for i in range(self.eslora)]
        else:
            fila = random.randint(0, tamano - self.eslora)
            col = random.randint(0, tamano - 1)
            posiciones = [(fila + i, col) for i in range(self.eslora)]

        self.coordenadas = posiciones
        return posiciones


# CLASE TABLERO
class Tablero:
    """
    Representa un tablero de Hundir la Flota con NumPy:
    - Crea una matriz de tamaño n x n
    - Coloca barcos sin solaparlos
    - Gestiona disparos y hundimientos
    """

    def __init__(self, tamano=10):
        self.tamano = tamano
        self.matriz = np.full((tamano, tamano), "~")
        self.barcos_coordenadas = []  # lista de listas, cada una con tuplas del barco
        self.ocupadas = set()
        self.libres = set()

    def puede_colocar(self, posiciones):
        """Verifica que las posiciones estén dentro del tablero y libres"""
        for fila, col in posiciones:
            if (fila, col) in self.ocupadas:
                return False
            if (fila, col) in self.libres:
                return False
            if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
                return False
        return True

    def casillas_alrededor(self, fila, col):
        """Devuelve las coordenadas alrededor de una casilla (incluye diagonales)."""
        alrededor = []
        for i in range(fila - 1, fila + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self.tamano and 0 <= j < self.tamano:
                    alrededor.append((i, j))
        return alrededor

    def barcos_en_tablero(self, posiciones):
        """Marca las posiciones de un barco en el tablero y añade sus alrededores a 'libres'."""
        for (fila, col) in posiciones:
            self.matriz[fila, col] = "B"
            self.ocupadas.add((fila, col))
            for (i, j) in self.casillas_alrededor(fila, col):
                if (i, j) not in self.ocupadas:
                    self.libres.add((i, j))

    def colocar_barco(self, eslora):
        """Crea y coloca un barco sin que se solape con otros"""
        colocado = False
        intentos = 0

        while not colocado and intentos < 1000:
            intentos += 1
            barco = Barco(eslora)
            posiciones = barco.generar_coordenadas(self.tamano)

            if self.puede_colocar(posiciones):
                self.barcos_en_tablero(posiciones)
                self.barcos_coordenadas.append(posiciones.copy())  # Añadimos una lista de tuplas
                colocado = True

        if not colocado:
            print(f"No se pudo colocar el barco de eslora {eslora}")

    def colocar_flota(self, flota):
        """Coloca una flota completa en el tablero"""
        for eslora in flota:
            self.colocar_barco(eslora)

    def disparar(self, fila, col):
        """Dispara a una celda y devuelve el resultado"""
        if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
            return "fuera"

        if self.matriz[fila, col] == "B":
            self.matriz[fila, col] = "X"
            self.actualizar_barcos((fila, col))
            return "tocado"
        elif self.matriz[fila, col] in ("X", "O"):
            return "repetido"
        else:
            self.matriz[fila, col] = "O"
            return "agua"

    def actualizar_barcos(self, coordenada):
        """Elimina coordenadas impactadas y detecta hundimientos"""
        for barco in self.barcos_coordenadas:
            if coordenada in barco:
                barco.remove(coordenada)
                if len(barco) == 0:
                    print("🔥 ¡Barco hundido!")
                    self.barcos_coordenadas.remove(barco)
                break

    def todos_hundidos(self):
        """True si todos los barcos han sido hundidos"""
        return len(self.barcos_coordenadas) == 0

    def mostrar(self, revelar=False):
        """Muestra el tablero"""
        if revelar:
            tablero_a_mostrar = self.matriz.copy()
        else:
            tablero_a_mostrar = np.where(self.matriz == "B", "~", self.matriz)

        print("   " + " ".join([chr(65 + c) for c in range(self.tamano)]))
        print("  " + "--" * self.tamano)
        for i, fila in enumerate(tablero_a_mostrar):
            print(f"{i:2} " + " ".join(fila))
        print()
