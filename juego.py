from utils import Tablero
import random


#funciones

#match letras numeros


def match_letras(letra):
    """Convierte letra A-J en índice 0-9"""
    dicc_col = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
    letra = letra.upper()
    if letra in dicc_col:
        return dicc_col[letra]
    else:
        return -1  # fuera de rangom

def pedir_coordenadas():
    """Pide al jugador fila y columna válidas"""
    valido = False
    while valido == False:
        try:
            print("Dispara")
            fila = int(input("Dime una fila (1-10): ")) - 1
            col = input("Dime una columna (A-J): ")
            col = match_letras(col)
            if fila < 0 or fila > 9 or col == -1: #comprobamos si no estan en el rango
                print("Coordenadas fuera de rango. Intenta de nuevo.")
            else:
                valido = True
        except ValueError:
            print("Entrada no válida. Intenta de nuevo.")
    return fila, col

def turno_jugador(tablero_enemigo):
    """Turno del jugador:
     -pìde coordenadas con la funcion 
     -usa el metodo disparar de tablero
     -con el resultado, decide si tocado o agua
     -comprueba si fuera o repetido
     -se basa en una variable jugar que cuando pasa a false acaba el turno
       """
    jugar = True
    while jugar == True:
        fila, col = pedir_coordenadas()
        resultado = tablero_enemigo.disparar(fila, col)
        
        if resultado == "tocado":
            print("Has tocado un barco!")
            tablero_enemigo.mostrar()
            # si todos los barcos del enemigo están hundidos, termina el juego
            if tablero_enemigo.todos_hundidos():
                return "ganado" #se acaba el while
            # si no, el jugador sigue disparando

        elif resultado == "agua":
            print("Has fallado. Agua.")
            tablero_enemigo.mostrar()
            jugar = False  # termina el turno del jugador

        elif resultado == "repetido":
            print("Ya habías disparado ahí. Prueba otra vez.")

        elif resultado == "fuera":
            print("Coordenadas fuera del tablero. Prueba otra vez.")

def turno_enemigo(tablero_jugador):
    """Turno de el enemigo
     -crea coordenadas random
     -usa el metodo disparar de tablero
     -con el resultado, decide si tocado o agua
     -comprueba si fuera o repetido
     -se basa en una variable jugar que cuando pasa a false acaba el turno
    """
    jugar = True
    while jugar == True:
        fila = random.randint(0, 9)
        col = random.randint(0, 9)
        resultado = tablero_jugador.disparar(fila, col)
        letra = match_letras(col)
        numero = fila + 1

        if resultado == "tocado":
            print(f"el enemigo dispara a {numero}{letra}: Tocado!")
            tablero_jugador.mostrar()
            # si todos los barcos del jugador están hundidos, termina el juego
            if tablero_jugador.todos_hundidos():
                return "perdido" #se acaba el while
            # si no, el enemigo sigue disparando

        elif resultado == "agua":
            print(f"el enemigo dispara a {numero}{letra}: Agua.")
            tablero_jugador.mostrar()
            jugar = False  # termina el turno de el enemigo

        elif resultado == "repetido":
            print(f"el enemigo dispara a {numero}{letra}: Repetido.")
            # intenta otra vez con nuevas coordenadas
            continue

        elif resultado == "fuera":
            print(f"el enemigo dispara a {numero}{letra}: Incorrecto.")
            # intenta otra vez
            continue

#juego

def jugar_partida():
    """Bucle principal de juego
    se dan las esloras de las flotas
    se crean los tableros
    se colocan las flotas
    se empieza a jugar
    """
    flota = [4,3,3,2,2,1,1]

    tablero_jugador = Tablero()
    tablero_enemigo = Tablero()

    tablero_jugador.colocar_flota(flota)
    tablero_enemigo.colocar_flota(flota)

    jugando = True
    print("Comienza la partida!\n")

    while jugando == True: #cuando jugando pase a ser false se acaba la partida
        print("TABLERO DEL JUGADOR")
        tablero_jugador.mostrar()
        print("TABLERO DEL ENEMIGO")
        tablero_enemigo.mostrar()

        # Turno del jugador
        print("\nTu turno:")
        estado = turno_jugador(tablero_enemigo)
        if estado == "ganado":
            print("Has ganado! Todos los barcos enemigos están hundidos.")
            jugando = False
            break

        # Turno del enemigo
        print("\nTurno del enemigo:")
        estado = turno_enemigo(tablero_jugador)
        if estado == "perdido":
            print("Has perdido. El enemigo ha hundido todos tus barcos.")
            jugando = False
            break


jugar_partida()