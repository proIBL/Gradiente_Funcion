from math import isnan
from sympy import symbols, diff, parse_expr, sympify, SympifyError
import numpy as np
import matplotlib.pyplot as plt


def verificar_formato1(cadena):
    if len(cadena) < 4:
        print("La cadena no es valida")
        exit(0)

    # Verificar si la cadena comienza con una letra seguida de paréntesis
    if not cadena[0].isalpha() or cadena[1] != '(':
        print("La cadena no es valida")
        exit(0)

    # Buscar el índice del cierre de paréntesis
    indice_cierre_parentesis = cadena.find(')')

    # Verificar si se encontró el cierre de paréntesis
    if indice_cierre_parentesis == -1:
        print("La cadena no es valida")
        exit(0)

    # Obtener la parte dentro de los paréntesis
    parametros = cadena[2:indice_cierre_parentesis]

    # Verificar si hay al menos una variable dentro de los paréntesis
    if len(parametros) == 0:
        print("La cadena no es valida")
        exit(0)

    signos_aritmeticos = {'+', '-', '*', '/', '(', ')'}

    for parameter in parametros.split(','):
        if parameter.isdigit() or parameter.strip() == '':
            print("La cadena no es valida")
            exit(0)
        for caracter in parameter:
            if caracter in signos_aritmeticos:
                print("La cadena no es valida")
                exit(0)


def verificar_formato2(cadena):
    if len(cadena) == 0:
        print("La cadena no es valida")
        exit(0)

    try:
        sympify(cadena)
        return True
    except SympifyError:
        print("La cadena no es valida")
        exit(0)


def verificar_formato3(punto):
    if len(punto) < 3:
        print("La cadena no es valida")
        exit(0)

    # Verificar si la cadena comienza con una letra seguida de paréntesis
    if punto[0] != '(':
        print("La cadena no es valida")
        exit(0)

    # Buscar el índice del cierre de paréntesis
    indice_cierre_parentesis = punto.find(')')

    # Verificar si se encontró el cierre de paréntesis
    if indice_cierre_parentesis == -1:
        print("La cadena no es valida")
        exit(0)

    parametros = punto[1:indice_cierre_parentesis]

    if len(parametros) == 0:
        print("La cadena no es valida")
        exit(0)

    for parameter in parametros.split(','):
        if not parameter.isdigit() or parameter.strip() == '':
            print("La cadena no es valida")
            exit(0)


def verificar_formato4(cadena, listavariables):
    if len(cadena) < 3:
        print("La cadena no es valida")
        exit(0)

    if cadena[0] != '(':
        print("La cadena no es valida")
        exit(0)

    indice_cierre_parentesis = cadena.find(')')

    if indice_cierre_parentesis == -1:
        print("La cadena no es valida")
        exit(0)

    if len(cadena.split(',')) != len(listavariables):
        print("La cadena no es valida")
        exit(0)

    coincidencia = 0
    for var1, var2 in zip(cadena.strip("()").split(','), listavariables):
        if var1 == var2:
            coincidencia += 1

    if coincidencia != 1:
        print("La cadena no es valida5")
        exit(0)


def funcion(entrada):
    verificar_formato2(entrada.split("=")[1])
    return entrada.split("=")[1]


def lista_variables(entrada):
    verificar_formato1(entrada.split("=")[0])
    return entrada.split("=")[0][1:].strip("()").split(",")


def seleccionarvariable(listavariables):
    print('Ingresa la variable a graficar, el resto dejalos constantes, en el orden que los introduciste por favor')
    cadena = input('Ejemplo (4,y,7) o (a,0,0)\n')
    verificar_formato4(cadena, listavariables)
    return cadena.strip("()").split(",")


def graficar(expresion, list_var, list_var_evalued,lista_derivadas):

    for elemento1, elemento2,elemento3 in zip(list_var, list_var_evalued,lista_derivadas):
        if elemento1 != elemento2:
            expresion = expresion.replace(elemento1, elemento2)
        else:
            derivada = str(elemento3)
            expresion = expresion.replace(elemento1, 'x')

    for elemento1, elemento2 in zip(list_var, list_var_evalued):
        if elemento1 != elemento2:
            derivada = derivada.replace(elemento1, elemento2)
        else:
            derivada = derivada.replace(elemento1, 'x')

    derivada = parse_expr(derivada)
    expresion = parse_expr(expresion)

    x_values = np.linspace(0, 10, 100)
    if expresion.is_number:
        y_values = np.full_like(x_values, expresion)
    else:
        y_values = np.array([expresion.subs('x', x) for x in x_values])

    if derivada.is_number:
        y_values2 = np.full_like(x_values, derivada)
    else:
        y_values2 = np.array([derivada.subs('x', x) for x in x_values])


    plt.plot(x_values, y_values,label='Función')
    plt.plot(x_values, y_values2, label='Derivada')
    plt.title('Gráfico de la funcion')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    print('Vamos a calcular un gradiente')
    entry_text = input('Escribe tu funcion de la manera f(x,y,z,...,n)=...\n')
    entry_text = entry_text.replace(" ", "")
    entry_text = entry_text.replace("^", "**")

    while entry_text.count("=") != 1:
        print('Expresion invalida')
        exit(0)
    lista_variables = lista_variables(entry_text)
    function = funcion(entry_text)

    vars_sym = symbols(lista_variables)
    gradiente_f = []
    expr = parse_expr(function)

    for var in vars_sym:
        derivada_parcial = diff(expr, var)
        gradiente_f.append(derivada_parcial)

    print('El gradiente es: ')
    print(gradiente_f)
    respuesta = input('¿Quieres evaluarlo en algun punto?\n')
    while respuesta == 'Si' or respuesta == 'SI' or respuesta == 'si':
        punto = input('¿en que punto te gustaría evaluarlo? escribelo en formato (x,y,z,...,n)\n')
        verificar_formato3(punto)
        lista_coordenadas_punto = punto.strip("()").split(",")

        while len(lista_variables) != len(lista_coordenadas_punto):
            print('Tienes que ingresar la misma cantidad de coordenadas que de variables ingreaste al inicio D:')
            punto = input('¿en que punto te gustaría evaluarlo? escribelo en formato (x,y,z,...,n)\n')
            lista_coordenadas_punto = punto.strip("()").split(",")
        diccionario = {}
        for clave, valor in zip(lista_variables, lista_coordenadas_punto):
            diccionario[clave] = valor
        gradiente_evaluado = []

        for expr1 in gradiente_f:
            valor_evaluado = expr1.evalf(subs=diccionario).evalf(n=3, chop=True)
            if isnan(valor_evaluado):
                gradiente_evaluado.append('indefinido')
            else:
                gradiente_evaluado.append(valor_evaluado)

        print('El gradiente evaluado en el punto es:')
        print(gradiente_evaluado)
        respuesta = input('Te gustaría evaluar en otro punto?\n')

    grafica = input('Te gustaria graficarlo?\n')
    while grafica == 'Si' or grafica == 'SI' or grafica == 'si':
        if len(lista_variables) == 1:
            graficar(function, lista_variables, lista_variables[0],gradiente_f)
        else:
            graficar(function, lista_variables, seleccionarvariable(lista_variables),gradiente_f)
        grafica = input('Quieres graficar otra vez?\n')
