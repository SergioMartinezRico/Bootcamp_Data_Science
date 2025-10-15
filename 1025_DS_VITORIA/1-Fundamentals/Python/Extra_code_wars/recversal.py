def solve(st):
 """
 la funcion calcula el numero de parentesis emparejados
 hay que recorrer un string viendo si cada parentesis abierto tiene cierre
 si encontramos uno abierto sumamos 1 a un contador
 si despues encontramos uno cerrado se resta 1 al contador
 caso especial, encontrar un cierre antes que haya una apertura
 en ese caso 
 """
 if len(st) % 2 != 0: 
    return -1  # imposible balancear

    stack = 0  # '(' abiertos sin cerrar
    unmatched_close = 0  # ')' sin abrir

    for c in st:
        if c == '(':
            stack += 1
        else:  # c == ')'
            if stack > 0:
                stack -= 1  # emparejamos
            else:
                unmatched_close += 1  # ')' sin pareja

    # cálculo de inversiones
    reversals = (stack // 2) + (unmatched_close // 2) + 2 * (stack % 2)
    return reversals
