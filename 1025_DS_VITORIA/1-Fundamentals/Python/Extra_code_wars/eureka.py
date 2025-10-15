def eureka(a, b):
    """
    la funcion haya numeros en una lista que cumplan la condicion a^1 + b^2 + c^3 = abc
    
    Iterar sobre todos los números entre a y b (inclusive).
Para cada número n:
Convertirlo en string para poder separar los dígitos.
Elevar cada dígito a la potencia de su posición (empezando en 1).
Sumar los resultados.
Si la suma coincide con el número → añadirlo a la lista de resultados.
Devolver la lista final.
    
    """


    resultados = []
    
    for n in range(a, b + 1):
        digitos = [int(d) for d in str(n)]  # convertir a lista de dígitos para usar enumerate
        suma = sum(d ** (i+1) for i, d in enumerate(digitos))  # elevar cada dígito a su posición
        if suma == n:
            resultados.append(n)  # cumple la propiedad
    
    return resultados
