import numpy as np
import random

#CLASE BARCO

class Barco:
    """
    Representa un barco:
     Tiene una eslora (tamaño)
     Guarda sus posiciones
     Registra los impactos recibidos
     
    """

    def __init__(self, eslora):
        self.eslora = eslora
        self.posiciones = []   # lista de tuplas (fila, columna)

    def asignar_posiciones(self, lista_posiciones):
        """Asigna las posiciones del barco"""
        self.posiciones = lista_posiciones.copy()


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
        self.barcos = []                    # lista de objetos Barco
        self.ocupadas = set()               # celdas ocupadas por algún barco. Set porque no se repiten
        self.libres = set()                 #celdas que tienen que quedar libres alrededor de cada barco
        self.barcos_coordenadas = []        # lista de listas de coordenadas (cada sublista = un barco)

#COMPROBAR SI SE PUEDE COLOCAR UN BARCO
    
    def puede_colocar(self, posiciones):
        """Verifica que las posiciones estén dentro del tablero y libres
        recibe una lista de posiciones. Verifica que no estan usadas 
        y que estan en rango
        """
        for fila, col in posiciones:
            if (fila, col) in self.ocupadas:  #coordenadas ocupadas
                return False
            if (fila, col) in self.libres: #casillas libres alrededor
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
            nuevo_barco = Barco(eslora) #llama a la clase Barco con un tamaño de eslora
            orientacion = random.choice("HV") #selecciona random la orientacion

            if orientacion == "H":
                fila = random.randint(0, self.tamano - 1) #primera coordenada de fila
                col = random.randint(0, self.tamano - eslora) #primera coordenada de columna
                posiciones_barco = [(fila, col + i) for i in range(eslora)] #lista de posiciones fila fija columna variable
            else:
                fila = random.randint(0, self.tamano - eslora)
                col = random.randint(0, self.tamano - 1)
                posiciones_barco = [(fila + i, col) for i in range(eslora)] #lista de posiciones columna fija fila variable

            if self.puede_colocar(posiciones_barco):
                nuevo_barco.asignar_posiciones(posiciones_barco)
                self.barcos_en_tablero(nuevo_barco)  #marca en el tablero y añade a lista de coordenadas
                self.barcos.append(nuevo_barco)       #guardamos objeto Barco
                colocado = True

        if not colocado:
            print(f"No se pudo colocar el barco de eslora {eslora}")

    def casillas_alrededor(self, fila, col):
            """Devuelve las coordenadas alrededor de una casilla (incluye diagonales)."""
            alrededor = []
            for i in range(fila - 1, fila + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.tamano and 0 <= j < self.tamano:
                        alrededor.append((i, j))
            return alrededor



    # MARCAR BARCO EN EL TABLERO
    
    def barcos_en_tablero(self, barco):
        """Marca las posiciones de un barco en el tablero y añade sus alrededores a 'libres'."""
        for (fila, col) in barco.posiciones:
            self.matriz[fila, col] = "B"
            self.ocupadas.add((fila, col))
            for (i, j) in self.casillas_alrededor(fila, col):
                if (i, j) not in self.ocupadas:  # Evita incluir la casilla del propio barco
                    self.libres.add((i, j))
        self.barcos_coordenadas.append(list(barco.posiciones))  #añadimos el barco como sublista


# DISPARAR
    
    def disparar(self, fila, col):
        """Dispara a una celda y devuelve el resultado
        Segun un par de coordenadas busca en el tablero. Si hay B, tocado
        Si no, Agua
        Tambien hay que capturar repeticiones y fueras de rango"""

        if self.matriz[fila, col] == "B":
            self.matriz[fila, col] = "X"
            
            # Buscar el barco impactado
            for sublista_barco in self.barcos_coordenadas:
                if (fila, col) in sublista_barco:
                    sublista_barco.remove((fila, col))  # quitamos la coordenada del barco
                    if not sublista_barco:
                        print("🔥 ¡Barco hundido!")
                        self.barcos_coordenadas.remove(sublista_barco)
                    break

            # Comprobamos si ya no quedan barcos
            if not self.barcos_coordenadas:
                print("🏁 ¡Todos los barcos han sido hundidos! Fin del juego.")
            return "tocado"

        elif self.matriz[fila, col] in ("X", "O"):
            return "repetido"
        else:
            self.matriz[fila, col] = "O"
            return "agua"
        if fila < 0 or fila >= self.tamano or col < 0 or col >= self.tamano:
            return "fuera"
        
        # REGISTRAR IMPACTO
    
    def barco_impacto(self, fila, col):
        """Incrementa el contador de impactos en el barco alcanzado"""
        for barco in self.barcos:
            if (fila, col) in barco.posiciones:
                barco.registrar_disparo(fila, col)
                break

    
    # COMPROBAR SI TODOS LOS BARCOS ESTÁN HUNDIDOS
    """True si todos los barcos han sido hundidos"""
    def todos_hundidos(self):
        return len(self.barcos_coordenadas) == 0

    
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
        self.tablero_jugador = Tablero(tamano) #creo los tableros
        self.tablero_cpu = Tablero(tamano)

        # Colocar flotas
        self.tablero_jugador.colocar_flota(flota) #aqui los tableros ya tienen los metodos de tablero
        self.tablero_cpu.colocar_flota(flota)

    #hace match de letras e index para las columnas

    def match_letras(self,letras):
        dicc_col={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
        columnas = dicc_col(upper(self.letras)) # type: ignore
        return columnas

    #hace match de numeros e index para las filas

    def match_num(self,numeros):
        filas = self.numeros-1
        return filas


    #turnos
    
    def turno_jugador(self):
        """El jugador dispara a la CPU"""
        while True:
            try:
                fila = int(input("Fila: (del 1 al 10) "))
                col = int(input("Columna: (de la A a la J) "))
                resultado = self.tablero_cpu.disparar(self.match_num(fila),self.match_num (col))
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
            resultado = self.tablero_jugador.disparar(self.match_num(fila),self.match_num (col))
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
                print("¡Has ganado! Todos los barcos enemigos están hundidos.")
                break

            # Turno de la CPU
            print("\nTurno de la CPU:")
            self.turno_cpu()

            if self.tablero_jugador.todos_hundidos():
                print(" Has perdido. La CPU ha hundido toda tu flota.")
                break
