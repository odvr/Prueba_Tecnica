
import decimal


# librerias requeridas

from sqlalchemy import Table, Column, Date, Float
# importacion del cong para la conexion con la base de datos
from config.db import meta, engine
from pydantic import BaseModel
from datetime import date
from sqlalchemy.types import Integer, Text, String, DateTime
from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT

from config.db import condb, session

app_prueba = APIRouter()


modelo_inventario = Table("prueba_tecnica", meta, Column("id_usuario", Integer, primary_key=True),
                                  Column("fecha_nacimiento", Date),
                                  Column("edad", Integer),
                                  Column("sexo", String(300)),
                                  Column("peso", Float),
                                  Column("comentario", String(300)))
meta.create_all(engine)

class Esquema_inventario(BaseModel):
    id_usuario : int
    fecha_nacimiento: date
    edad: int
    sexo :str
    peso: float
    comentario : str
      #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"





"""
1. Crea una función que tome un número como entrada y devuelva "Fizz" si el número es
divisible por 3, "Buzz" si es divisible por 5 y "FizzBuzz" si es divisible por ambos. En caso
contrario, la función debe devolver el número. (0.5 punto)
"""

def funcion_numero(divisible):
    if divisible % 5 == 0 and divisible % 3 == 0:
        print("FizzBuzz")

    elif divisible % 3 == 0:
        print("Fizz")

    elif divisible % 5 == 0:
        print("Buzz")

    else:
        print(divisible)

    return

#Variable_Funcion_Numero= int (input("Ingresa el Numero para el Primer Punto: "))
#funcion_numero(Variable_Funcion_Numero)

"""
2. Crea una función que tome una lista de números como entrada y devuelva la suma de todos
los números pares en la lista. (0.5 punto)
"""

def suma_numeros_pares(lista):
    suma = 0
    for numero in lista:
        if numero % 2 == 0:
            suma += numero
    return suma
#numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#resultado = suma_numeros_pares(numeros)
#print(resultado)


"""
Escribe una función que tome una cadena de texto como entrada y devuelva el número de
palabras que contiene. Se considera que una palabra es cualquier secuencia de caracteres
separada por espacios.
"""

def contar_palabras(cadena):
    palabras = cadena.split()
    return len(palabras)
texto = "Primera Segunda Tercera"
resultado_palabras = contar_palabras(texto)
#print(resultado_palabras)


"""4. Crea una función que tome una lista de números y devuelva la lista ordenada de forma
ascendente sin usar la función sort(). Puedes implementar cualquier algoritmo de ordenamiento
que desees."""

def ordenar_lista(lista):
    for i in range(len(lista)):
        min = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[min]:
                min_ = j
        lista[i], lista[min_] = lista[min], lista[i]
    return lista
numeros = [9, 5, 2, 7, 1, 8, 3, 6, 4]
resultado = ordenar_lista(numeros)
#print(resultado)



"""
5. Escribe una función que tome un número como entrada y devuelva la suma de todos los
números naturales menores o iguales a ese número que son múltiplos de 3 o 5.
"""

def suma_multiplos(numero):
    suma = 0
    for i in range(1, numero + 1):
        if i % 3 == 0 or i % 5 == 0:  # Comprueba si el número es múltiplo de 3 o 5
            suma += i
    return suma

numero_multiplos = 20
resultado = suma_multiplos(numero_multiplos)
#print(resultado)


"""
6. Crea una función que tome dos listas como entrada y devuelva una lista que contenga todos
los elementos que se encuentran en ambas listas.
"""

def elementos_comunes(lista1, lista2):
    elementos = []
    for elemento in lista1:
        if elemento in lista2:  # Comprueba si el elemento está presente en ambas listas
            elementos.append(elemento)
    return elementos

lista1 = [1, 2, 3, 4, 5]
lista2 = [4, 5, 6, 7, 8]
resultado_agregar_litas = elementos_comunes(lista1, lista2)
#print(resultado_agregar_litas)



"""
Escribe una función que tome una cadena de texto como entrada y devuelva la misma cadena
de texto invertida.
"""
def invertir_cadena(cadena):
    cadena_invertida = cadena[::-1]
    return cadena_invertida

texto = "H"
resultado_invertir_cadena = invertir_cadena(texto)
#print(resultado_invertir_cadena)

"""
8. Crea una función que tome un número como entrada y devuelva el factorial de ese número.
El factorial de un número es el producto de todos los enteros positivos desde 1 hasta el número
en cuestión.
"""
def factorial(numero):
    if numero == 0:  # Caso base: factorial de 0 es 1
        return 1
    else:
        factorial = 1
        for i in range(1, numero + 1):
            factorial *= i
        return factorial

numero = 5
resultadoFactorial = factorial(numero)
#print(resultadoFactorial)

"""
9. implementa un Crud web, conectado a una base de datos (motor de elección de su interés)
que permita insertar, modificar, eliminar y consultar 3 campos numericos, 2 campos de texto y
1 campo de fecha.
"""


@app_prueba.get("/Consultar", response_model=list[Esquema_inventario]
                   )
async def inventario_bovino():


    try:
        items = condb.execute(modelo_inventario.select()).fetchall()


    except Exception as e:

        raise
    finally:
        condb.close()

    return items





@app_prueba.post("/Crear", status_code=HTTP_204_NO_CONTENT)
async def Crear(esquemaInventario: Esquema_inventario):


    try:
        inventario_dic = esquemaInventario.dict()
        ingreso = modelo_inventario.insert().values(inventario_dic)
        condb.execute(ingreso)

        condb.commit()
    except Exception as e:

        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)

"""
"""
@app_prueba.put("/cambiar_datos/{id_usuario}", status_code=HTTP_204_NO_CONTENT)
async def cambiar_esta_bovino(data_update: Esquema_inventario, id_usuario: str):
    try:
        condb.execute(modelo_inventario.update().values(
            fecha_nacimiento=data_update.fecha_nacimiento, sexo=data_update.sexo,
            peso=data_update.peso, edad=data_update.edad,
            comentario=data_update.comentario).where(
            modelo_inventario.columns.id_usuario == id_usuario))

        condb.commit()



    except Exception as e:

        raise

    finally:
        condb.close()

    return Response( status_code=HTTP_204_NO_CONTENT)


@app_prueba.delete("/Eliminar/{id_usuario}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino(id_usuario: str):

    try:
        condb.execute(modelo_inventario.delete().where(modelo_inventario.c.id_usuario == id_usuario))
        condb.commit()

    except Exception as e:

        raise
    finally:
        condb.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)
