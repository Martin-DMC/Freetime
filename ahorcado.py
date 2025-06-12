#!/usr/bin/python3
import random
import os

def secret_word():
    palabras = [('amarillo'), ('rojo'), ('verde'), ('negro')]
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


vidas = 7
palabra = secret_word()
pal_jug = word_player(palabra)
matrx = [[' ', ' ', ' '],
[' ', ' ', ' '],
[' ', ' ', ' '],
[' ', ' ', ' ']]
limpiar()
bienvenida()
while True or vidas > 0:
    limpiar()
    print_tablero(matrx)
    print("\ntu palabra")
    cadena_jug = "".join(pal_jug)
    print(cadena_jug)
    letra = input("\ningresa una letra: ")
    asierto = 1
    if not letra in palabra:
        vidas -= 1        
    for i, let in enumerate(palabra):
        if let == letra:
            pal_jug[i] = let
        else:
            if pal_jug[i] != '-':
                pal_jug[i] == pal_jug[i]
            else:
                pal_jug[i] = '-'
    llenar_matrix(matrx, vidas)
    input("pres enter")
