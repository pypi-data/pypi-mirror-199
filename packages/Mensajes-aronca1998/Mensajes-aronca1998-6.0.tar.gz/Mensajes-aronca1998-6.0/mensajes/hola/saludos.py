import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

class Saludo:
    def __init__(self):
        print("Te saludo desde Saludo.__init__")

if __name__== "__main__":
    saludar()

def prueba():
    print("Esto es una prueba de la nueva versión")
def generar_array(numeros):
    return np.arange(numeros)