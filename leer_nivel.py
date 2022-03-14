import os
from io import open
#leer niveles por bloc de notas
def LeerLineaPorLinea(archivo):
    #crear la lista de contenido
    lista_str=[]
    lista_buffer=[]
    lista_int=[]
    #abrir el archivo y pasar por cada una de sus filas
    with open(archivo) as f:
        for linea in f:
            #leer linea por linea el arreglo
            lista_str=([elt.strip() for elt in linea.split(',')])
            #convertirlos en numeros y no en str
            lista_buffer=[]
            for numero in lista_str:
                lista_buffer.append(int('0'+numero))
            lista_int.append(lista_buffer)

    return lista_int

def EscanearMapa(archivo):
    leer_nivel=[]
    #si el mapa no existe crearlo
    if not os.path.exists(archivo):
        pass
    else:
        #leer el archivo
        leer_nivel=LeerLineaPorLinea(archivo)
    return leer_nivel


#leer niveles para modificarlos
def EditarNivel(archivo):
    EscanearMapa(archivo)


#EditarNivel(archivo)
