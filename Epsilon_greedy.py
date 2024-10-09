'''En el caso de estudio tenemos:
Parcelas: Tenemos 3 parcelas de cultivos diferentes.
Acciones: Cada parcela puede recibir una cantidad diferente de agua (estrategias de riego indicadas por el cliente).

El sistema explora nuevas estrategias de riego un porcentaje del tiempo (Usaré el algoritmo Epsilon-Greedy) y explota la mejor estrategia conocida el resto del tiempo. 
El rendimiento de cada parcela depende de la estrategia aplicada y tiene variabilidad.

Para validar el código, usaremos random, si funciona se pasará con datos reales'''

#Código
import numpy as np
import random

# Definir el número de parcelas y estrategias de riego
parcelas = ['Parcela A', 'Parcela B', 'Parcela C']
estrategias_riego = ['Bajo riego', 'Riego moderado', 'Riego alto']

# Parámetros del Multi-Armed Bandit
epsilon = 0.1  # Tasa de exploración (10%), explotación (90%)
recompensas_esperadas = np.zeros((len(parcelas), len(estrategias_riego)))  # Recompensas esperadas
cuentas_seleccion = np.zeros((len(parcelas), len(estrategias_riego)))  # Cuenta de veces que se ha seleccionado cada acción

# Función que simula el rendimiento en función de la estrategia de riego aplicada
def obtener_rendimiento(parcela, estrategia):
    # Resultados simulados para el rendimiento agrícola en cada parcela
    # Vamos a simular que el rendimiento es mayor para una estrategia en particular
    rendimiento_base = {
        'Parcela A': [0.5, 0.7, 0.9],  # Estrategias de riego: bajo, moderado, alto
        'Parcela B': [0.4, 0.8, 0.6],
        'Parcela C': [0.6, 0.9, 0.7]
    }
    
    # Introducimos una variación aleatoria (representa las condiciones climáticas)
    variacion = np.random.normal(0, 0.05)
    
    return rendimiento_base[parcela][estrategia] + variacion

# Función para seleccionar la mejor estrategia de riego utilizando Epsilon-Greedy
def seleccionar_estrategia(parcela_idx):
    if random.random() < epsilon:
        # Exploración: elegir una estrategia aleatoria
        return random.randint(0, len(estrategias_riego) - 1)
    else:
        # Explotación: elegir la mejor estrategia basada en recompensas esperadas
        return np.argmax(recompensas_esperadas[parcela_idx])

# Simulación del riego y aprendizaje con Multi-Armed Bandit
def optimizar_riego(iteraciones=1000):
    for i in range(iteraciones):
        # Elegir una parcela al azar
        parcela_idx = random.randint(0, len(parcelas) - 1)
        parcela = parcelas[parcela_idx]

        # Seleccionar la mejor estrategia para esa parcela
        estrategia_idx = seleccionar_estrategia(parcela_idx)
        estrategia = estrategias_riego[estrategia_idx]

        # Obtener el rendimiento para esa parcela y estrategia
        rendimiento = obtener_rendimiento(parcela, estrategia_idx)

        # Actualizar las cuentas y recompensas esperadas
        cuentas_seleccion[parcela_idx, estrategia_idx] += 1
        n = cuentas_seleccion[parcela_idx, estrategia_idx]
        recompensa_actual = recompensas_esperadas[parcela_idx, estrategia_idx]
        recompensas_esperadas[parcela_idx, estrategia_idx] = recompensa_actual + (rendimiento - recompensa_actual) / n
        
        # Imprimir resultados ocasionales
        if i % 100 == 0:
            print(f"Iteración {i}: Estrategia '{estrategia}' aplicada en '{parcela}', rendimiento: {rendimiento:.2f}")

# Ejecutar la simulación de optimización de riego
optimizar_riego()

# Mostrar las recompensas esperadas finales
for i, parcela in enumerate(parcelas):
    print(f"\nRecompensas esperadas para {parcela}:")
    for j, estrategia in enumerate(estrategias_riego):
        print(f"  Estrategia '{estrategia}': {recompensas_esperadas[i, j]:.2f}")
