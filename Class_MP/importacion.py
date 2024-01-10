import sys 
import os

def modulo_padre():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    directorio_proyecto = os.path.join(directorio_actual, os.pardir)
    sys.path.append(directorio_proyecto)