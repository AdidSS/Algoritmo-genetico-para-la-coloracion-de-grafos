import random
import time
import networkx as nx
import matplotlib.pyplot as plt
start = time.time()
G = nx.Graph()
G.add_nodes_from(range(1,20))
#Cromosoma: Numerico (cada numero = color)
#Longitud: n = # de nodos = 19
numNodos = 19
#Poblacion 1000
tamPoblacion = 1000
#Inicializacion Aleatorios (un color por cada nodo)
#Infactibilidad No
#Paro 100,000
iteraciones = 100000
#Fitness n/c
def fitness_factibles(lista):
    nuevoSet = set(lista)
    colores = len(nuevoSet)
    return 1/colores

def repetidos(lista):
    numerosRepetidos = set()  # Use a set to store repeated values (no duplicates)
    
    for nodo, conexiones in vecinos.items():
        for vecino in conexiones:
            # Check if the value of the current node is the same as any of its neighbors
            if lista[nodo - 1] == lista[vecino - 1]:
                numerosRepetidos.add(lista[nodo - 1])
    
    return len(numerosRepetidos)

def fitness_infactibles(lista):
    nuevoSet = set(lista)
    colores = len(nuevoSet)
    numerosRepetidos = repetidos(lista)
    return 1/(colores+numerosRepetidos)
#Seleccion: Ruleta
#Probabilidad de cruce: 1
probCruce = 1
#Puntos de cruce: 2
#Lugar de cruce: 6, 12
#Probabilidad de mutacion: 0.05
probMutacion = 0.05
#Criterio Reemplazo: Sustitucion peores de la poblacion.
#Ejemplo
vecinos = {
       1: [2, 4, 16],
    2: [1, 3, 4, 5, 6, 7],
    3: [2, 7, 19],
    4: [1, 2, 5, 8, 9],
    5: [2, 4, 6, 9, 10],
    6: [2, 5, 7, 11, 14],
    7: [2, 3, 6, 11],
    8: [4, 9, 12, 16],
    9: [4, 5, 8, 10, 12, 13, 15],
    10: [5, 9, 13, 14],
    11: [3, 6, 7, 14, 19],
    12: [8, 9, 15, 16],
    13: [9, 10, 14, 15, 17, 18],
    14: [6, 10, 11, 13, 18, 19],
    15: [9, 12, 13, 16, 17],
    16: [1, 8, 12, 15, 17],
    17: [13, 15, 16, 18, 19],
    18: [13, 14, 17, 19],
    19: [3, 11, 14, 17, 18]
}
# Agregar las aristas
for nodo, nodos_conectados in vecinos.items():
    for nodo_conectado in nodos_conectados:
        G.add_edge(nodo, nodo_conectado)


colores = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta',
           'lime', 'pink', 'brown', 'gray', 'olive', 'navy', 'teal', 'maroon', 'gold', 'indigo', 'turquoise']
#Validaciones:
#for item in poblacion:
    #print(item)
def normalizacion(lista, sumaTotal):
    normalizados = []
    for valor in lista:
        normalizados.append(valor/sumaTotal)
    return normalizados

#tmp = 0
#for resultado in fitnessNormalizada:
    #tmp += resultado
#print(tmp)
def probabilidadAcumulada(listaProbabilidades):
    lista = []
    acum = 0
    for i in range (len(listaProbabilidades)):
        acum += listaProbabilidades[i]
        lista.append(acum)
    return lista

def mutacion(cromosoma):
    num = random.random()
    cromosoma_mutado = cromosoma.copy()
    for i in range(len(cromosoma)):
        if num <= probMutacion:
            cromosoma_mutado[i] = random.randint(1,19)  
    return cromosoma_mutado

def cruce(padre1,padre2):
    hijo1 = padre1[:6] + padre2[6:12]+padre1[12:] 
    hijo2 = padre2[:6] + padre1[6:12] + padre2[12:]
    return hijo1, hijo2

##Programa:
#Generacion de poblacion inicial
def seleccionar_padre(lista_probabilidad_acumulada):
    valor = random.random()
    for i in range(len(lista_probabilidad_acumulada)):
        if valor <= lista_probabilidad_acumulada[i]:
            return i
            
        else:
            return len(lista_probabilidad_acumulada) - 1

# Initialization of population and other variables
poblacion = []
for p in range(tamPoblacion):
    individuo = []  
    for i in range(numNodos):
        color = random.randint(1, 19)
        individuo.append(color)

    poblacion.append(individuo)  # Add the individual to the population list

# Calculation of fitness
calculoFitness = []
for individuo in poblacion:
    if repetidos(individuo) > 0:
        fitness_1 = fitness_infactibles(individuo)
    else:
        fitness_1 = fitness_factibles(individuo)
    calculoFitness.append(fitness_1)

total = sum(calculoFitness)

fitnessNormalizada = normalizacion(calculoFitness, total)
acumulada = probabilidadAcumulada(fitnessNormalizada)

# Parent selection and crossover
padre1 = poblacion[seleccionar_padre(acumulada)]
padre2 = poblacion[seleccionar_padre(acumulada)]
hijo1, hijo2 = cruce(padre1, padre2)
cromosoma_mutado1 = mutacion(hijo1)
cromosoma_mutado2 = mutacion(hijo2)

if repetidos(cromosoma_mutado1) > 0:
    fitness_1 = fitness_infactibles(cromosoma_mutado1)
else:
    fitness_1 = fitness_factibles(cromosoma_mutado1)

if repetidos(cromosoma_mutado2) > 0:
    fitness_2 = fitness_infactibles(cromosoma_mutado2)
else:
    fitness_2 = fitness_factibles(cromosoma_mutado2)

while i < iteraciones:
    if fitness_1 > min(calculoFitness):
        # Sustituyo
        min_pos = calculoFitness.index(min(calculoFitness))
        calculoFitness[min_pos] = fitness_1
        poblacion[min_pos] = cromosoma_mutado1

    if fitness_2 > min(calculoFitness):
        # Sustituyo
        min_pos = calculoFitness.index(min(calculoFitness))
        calculoFitness[min_pos] = fitness_2
        poblacion[min_pos] = cromosoma_mutado2

    else:
        mejor_sol = max(calculoFitness)    

    # Generacion de nuevos hijos
    padre1 = poblacion[seleccionar_padre(acumulada)]
    padre2 = poblacion[seleccionar_padre(acumulada)]
    hijo1, hijo2 = cruce(padre1,padre2)
    cromosoma_mutado1 = mutacion(hijo1)
    cromosoma_mutado2 = mutacion(hijo2)
    if repetidos(cromosoma_mutado1) > 0:
        fitness_1 = fitness_infactibles(cromosoma_mutado1)
    else:
        fitness_1 = fitness_factibles(cromosoma_mutado1)
    if repetidos(cromosoma_mutado2) > 0:
        fitness_2 = fitness_infactibles(cromosoma_mutado2)
    else:
        fitness_2 = fitness_factibles(cromosoma_mutado2)
    i += 1
# Despues de sustituir cromosomas
print('Minimo:', min(calculoFitness), '\nMaximo:', max(calculoFitness))

max_pos = calculoFitness.index(max(calculoFitness))
print('Cromosoma:',poblacion[max_pos])
print('Funcion fitness:',fitness_factibles(poblacion[max_pos]))

mejor_sol = 0

mejor_sol = fitness_factibles(poblacion[max_pos])
poblacion_max_pos = poblacion[max_pos]
print('Mejor solucion tiene una funcion objetivo de:', mejor_sol)
end = time.time()
tiempo = end-start
# Crear una lista de colores para cada nodo
node_colors = [colores[poblacion_max_pos[i] - 1] for i in range(len(poblacion_max_pos))]

# Dibujar el grafo con los colores asignados a los nodos
nx.draw(G, with_labels=True, node_color=node_colors, edge_color='gray', node_size=1000, font_size=12)

# Mostrar el grafo
plt.show()
print("Tiempo de : ", tiempo, "segundos")