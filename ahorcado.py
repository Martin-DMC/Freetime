#!/usr/bin/python3
import random
import os

def secret_word():
    palabras = [('terminator'), ('avatar'), ('chuky'), ('casocerrado'), ('elconjuro'), ('superman')]
    ran = random.randint(0, len(palabras) - 1)
    palabra = palabras[ran]
    return palabra

def word_player(palabra):
    palabra_jugador = list('-' * len(palabra))
    return palabra_jugador

def llenar_matrix(matrix, vidas):
    if vidas == 6:
        matrix[3][2] = "\\"
    elif vidas == 5:
        matrix[3][0] = '/'
    elif vidas == 4:
        matrix[2][2] = '\\'
    elif vidas == 3:
        matrix[2][1] = '|'
    elif vidas == 2:
        matrix[2][0] = '/'
    elif vidas == 1:
        matrix[1][1] = 'O'
    elif vidas == 0:
        matrix[0][1] = '|'
    return matrix

def bienvenida():
    print("""          **********
          *ahorcado*
          **********

        press enter
""")
    input("")

def limpiar():
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

def print_tablero(matrix):
    for fila in matrix:
        ret = "".join(fila)
        print(ret)

def check_word(palabra, palabra1):
    if palabra == palabra1:
        return True
    else:
        return False

def salir():
    op = input("[s] para salir, [enter] para continuar")
    if op == 's':
        return True
    else:
        return False

vidas = 7
i = 0
letras_usadas = []
palabra = secret_word()
pal_jug = word_player(palabra)
matrx = [[' ', ' ', ' '],
[' ', ' ', ' '],
[' ', ' ', ' '],
[' ', ' ', ' ']]
limpiar()
bienvenida()
while i < 100 and vidas > 0:
    limpiar()
    cadena_jug = "".join(pal_jug)
    if check_word(palabra, cadena_jug) is True:
        print("""\n\n        *************
        * you win!! *
        *************""")
        break
    else:
        pass
    print_tablero(matrx)
    if i != 0:
        print("letras usadas")
        print(letras_usadas) 
    print("\ntu palabra")
    print(cadena_jug)
    letra = input("\ningresa una letra: ")
    while True:
        if letra in letras_usadas:
            letra = input("\nletra ya ingresada: ")
        else:
            break
        limpiar()
    if not letra in palabra:
        vidas -= 1
        letras_usadas.append(letra)
    for i, let in enumerate(palabra):
        if let == letra:
            pal_jug[i] = let
        else:
            if pal_jug[i] != '-':
                pal_jug[i] == pal_jug[i]
            else:
                pal_jug[i] = '-'
    llenar_matrix(matrx, vidas)
    if salir() is True:
        break
    else:
        continue
if vidas == 0:
    llenar_matrix(matrx, vidas)
    limpiar()
    print_tablero(matrx)
    print("you lose. BUUHHH!!!")