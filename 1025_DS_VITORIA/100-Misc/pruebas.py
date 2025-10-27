import numpy as np
import random


#CLASE BARCO

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
        self.posiciones = []   # lista de tuplas (fila, columna)
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
        


# CLASE TABLERO
class Tablero:
    """
    Representa un tablero de Hundir la Flota con NumPy:
    - Crea una matriz de tamaño n x n
    - Coloca barcos sin solaparlos
    - Gestiona disparos y hundimientos
    """
    # CREAR TABLERO
    
    def __init__(self, tamano=10):
        self.tamano = tamano
        self.matriz = np.full((tamano, tamano), "~")
        self.barcos = []        # lista de objetos Barco
        self.ocupadas = set()   # celdas ocupadas por algún barco. Set porque no se repiten

    #COMPROBAR SI SE PUEDE COLOCAR UN BARCO
    
    def puede_colocar(self, posiciones):
        """Verifica que las posiciones estén dentro del tablero y libres
        recibe una lista de posiciones. Verifica que no estan usadas 
        y que estan en rango
        """
        for fila, col in posiciones:
            if (fila, col) in self.ocupadas:  #coordenadas ocupadas
                return False
            if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:    #coordenadas fuera de rango
                return False
        return True

    
    # COLOCAR UN BARCO
    
    def colocar_barco(self, eslora):
        """Crea y coloca un barco sin que se solape con otros"""
        colocado = False
        intentos = 0

        while not colocado and intentos < 1000:  # evita bucles infinitos. Cuando colocado sea True, para el bucle por hacerse false
            intentos += 1
            barco = Barco(eslora) #llama a la clase Barco con un tamaño de eslora
            orientacion = random.choice("HV") #selecciona random la orientacion

            if orientacion == "H":
                fila = random.randint(0, self.tamano - 1) #primera coordenada de fila
                col = random.randint(0, self.tamano - eslora) #primera coordenada de columna
                posiciones = [(fila, col + i) for i in range(eslora)] #lista de posiciones fila fija columna variable
            else:
                fila = random.randint(0, self.tamano - eslora)
                col = random.randint(0, self.tamano - 1)
                posiciones = [(fila + i, col) for i in range(eslora)] #lista de posiciones columna fija fila variable

            if self.puede_colocar(posiciones):
                barco.posiciones = posiciones  #rellena la lista de posiciones del barco
                self.barcos_en_tablero(barco)  #activa la clase barcos en tablero. Rellena el tablero con B
                self.barcos.append(barco)    #rellena la lista de barcos. Es una lista de coordenadas
                colocado = True

        if not colocado:
            print(f"No se pudo colocar el barco de eslora {eslora}")


    # COLOCAR FLOTA COMPLETA
    
    def colocar_flota(self, lista_esloras):
        """Coloca todos los barcos definidos en la lista
        Bucle de la clase colocar_barco iterando sobre la lista
        de esloras de los barcos a colocar"""
        for eslora in lista_esloras:
            self.colocar_barco(eslora)


    # MARCAR BARCO EN EL TABLERO
    
    def barcos_en_tablero(self, barco):
        """Marca las posiciones de un barco en el tablero"""
        for (fila, col) in barco.posiciones:
            self.matriz[fila, col] = "B"
            self.ocupadas.add((fila, col))

    
    # DISPARAR
    
    def disparar(self, fila, col):
        """Dispara a una celda y devuelve el resultado
        Segun un par de coordenadas busca en el tablero. Si hay B, tocado
        Si no, Agua
        Tambien hay que capturar repeticiones y fueras de rango"""

        if self.matriz[fila, col] == "B":
            self.matriz[fila, col] = "X"  # tocado
            self.barco_impacto(fila, col)
            return "tocado"
        elif self.matriz[fila, col] in ("X", "O"):
            return "repetido"
        else:
            self.matriz[fila, col] = "O"  # agua
            return "agua"
        if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
            return "fuera"


    
    # REGISTRAR IMPACTO
    
    def barco_impacto(self, fila, col):
        """Incrementa el contador de impactos en el barco alcanzado"""
        for barco in self.barcos:
            if (fila, col) in barco.posiciones:
                barco.registrar_disparo()
                break

    
    # COMPROBAR SI TODOS LOS BARCOS ESTÁN HUNDIDOS
    """True si todos los barcos han sido hundidos"""
    def todos_hundidos(self):
        hundidos = True
        for barco in self.barcos:
            if  barco.hundido() == False:
                hundidos = False
            break
        return hundidos

    
    # MOSTRAR TABLERO 
    def mostrar(self, revelar=False):
        """
        Muestra el tablero:
        - Si revelar=False, oculta los barcos ('B' → '~')
        - Usa funciones NumPy para hacerlo más limpio
        """
        if revelar:
            tablero_a_mostrar = self.matriz.copy()
        else:
            tablero_a_mostrar = np.where(self.matriz == "B", "~", self.matriz)

        print("   " + " ".join([str(c) for c in range(self.tamano)]))
        print("  " + "--" * self.tamano)
        for i, fila in enumerate(tablero_a_mostrar):
            print(f"{i:2} " + " ".join(fila))
        print()



# CLASE PARTIDA

class Partida:
    """
    Gestiona una partida entre el jugador y la CPU:
    - Cada uno tiene su tablero
    - Se alternan los disparos
    - Gana quien hunda toda la flota rival
    """

    def __init__(self, tamano=10, flota=[4, 3, 3, 2, 2, 1, 1]):
        self.tamano = tamano
        self.flota = flota

        # Crear tableros
        self.tablero_jugador = Tablero(tamano)
        self.tablero_cpu = Tablero(tamano)

        # Colocar flotas
        self.tablero_jugador.colocar_flota(flota)
        self.tablero_cpu.colocar_flota(flota)

    def turno_jugador(self):
        """El jugador dispara a la CPU"""
        while True:
            try:
                fila = int(input("Fila: "))
                col = int(input("Columna: "))
                resultado = self.tablero_cpu.disparar(fila, col)
                print(f"Resultado: {resultado}\n")
                if resultado != "repetido":
                    break
            except ValueError:
                print("Introduce números válidos.")

    def turno_cpu(self):
        """La CPU dispara de forma aleatoria"""
        while True:
            fila = random.randint(0, self.tamano - 1)
            col = random.randint(0, self.tamano - 1)
            resultado = self.tablero_jugador.disparar(fila, col)
            if resultado != "repetido":
                print(f"CPU dispara a ({fila},{col}): {resultado}")
                break

    def jugar(self):
        """Ejecuta el bucle principal de juego"""
        print("=== ¡Comienza la partida! ===\n")

        while True:
            print("=== TABLERO DEL JUGADOR ===")
            self.tablero_jugador.mostrar(revelar=True)

            print("=== TABLERO DEL ENEMIGO ===")
            self.tablero_cpu.mostrar(revelar=False)

            # Turno del jugador
            print("Tu turno:")
            self.turno_jugador()

            if self.tablero_cpu.todos_hundidos():
                print("🏆 ¡Has ganado! Todos los barcos enemigos están hundidos.")
                break

            # Turno de la CPU
            print("\nTurno de la CPU:")
            self.turno_cpu()

            if self.tablero_jugador.todos_hundidos():
                print("💀 Has perdido. La CPU ha hundido toda tu flota.")
                break
