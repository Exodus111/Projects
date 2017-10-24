#!/usr/bin/python3

import numpy as np
import random
import sys
import select


def main(matrix, maxfs=200, maxcountrep=5000, alpha=0.99, min_temp=0.001):

    poblacion = first_solutions(matrix, maxfs, maxcountrep)
    really_best_sol = poblacion[0]
    really_best_fit = fitness(matrix, really_best_sol)
    print('Colores utilizados por población generada: {}'.format(
        str(len(set(really_best_sol)))))
    for i, sol in enumerate(poblacion):
        print('Reseteo con first solution # {}'.format(str(i + 1)))
        new_best_sol, new_best_fit = enfriamiento(matrix, sol, min_temp, alpha)
        if new_best_fit > really_best_fit:
            really_best_sol = new_best_sol
            really_best_fit = new_best_fit
            print('MEJORA GLOBAL. Colores: {}'.format(
                str(len(set(really_best_sol)))))
            if check(3):
                return(really_best_sol, really_best_fit)

        if (i + 1) % 5 == 0:
            if check(3):
                return(really_best_sol, really_best_fit)

    return(really_best_sol, really_best_fit)


def check(waittime):
    print("Pulsa cualquier tecla y enter para parar la ejecución del algoritmo.")
    i, o, e = select.select([sys.stdin], [], [], waittime)

    if (i):
        return(True)
    else:
        return(False)


def first_solutions(matrix, maxfs, maxcountrep):
    '''Inicializa las primeras soluciones. matrix ha de ser np.array'''
    N = matrix.shape[0]

    # Miro que nodos tienen el máximo grado.
    # Almaceno sus índices en max_nodes
    vector_degrees = np.array([sum(row) for row in matrix])
    max_degrees = vector_degrees.max()
    max_nodes = [vector_degrees.argmax()]

    if max_nodes[-1] + 1 != len(vector_degrees):
        while vector_degrees[max_nodes[-1] + 1:].max() == max_degrees:
            max_nodes.append(
                vector_degrees[max_nodes[-1] + 1:].argmax() + max_nodes[-1] + 1)
            if max_nodes[-1] + 1 == len(vector_degrees):
                break

    solutions = []  # Vector de soluciones (matriz)
    countrep = 0  # Cuenta las veces que se repite una solución
    r = random.Random()

    while len(solutions) < maxfs and countrep < maxcountrep:
        # Primero escojo uno de los nodos con más vértices al azar.
        r.seed()
        first_node = r.choice(max_nodes)
        colors_fn = list(range(1, max_degrees + 1))
        solution = list(np.zeros(N))

        # Coloreamos el nodo elegido y sus vecinos
        for i, nb in enumerate(matrix[first_node]):
            if nb == 1:
                solution[i] = r.choice(colors_fn)
                colors_fn.remove(solution[i])

        # Coloreamos los demás nodos
        for node, col_node in enumerate(solution):
            if col_node == 0:
                colors = list(range(1, max_degrees + 1))

                for k, nb in enumerate(matrix[node]):
                    if nb == 1 and solution[k] != 0:
                        if solution[k] in colors:
                            colors.remove(solution[k])

                solution[node] = r.choice(colors)

        # Si la solución ya existe sumamos 1 al contador, en caso contrario la añadimos
        if solution in solutions:
            countrep += 1
        else:
            solutions.append(list(solution))

    return(solutions)


def fitness(matrix, solution):
    '''Calcula el valor fitnees de solution'''
    f1 = 1 / len(set(solution))
    f2 = 0
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            if matrix[i, j] == 1:
                if solution[i] == solution[j]:
                    f2 += 1
    fit = f1 - f2
    return(fit)

counter = 0
def enfriamiento(matrix, solution, min_temp, alpha):
	global counter
	best_sol = solution
	best_fit = fitness(matrix, solution)
	n = len(solution)
	temp = 1
	cambio = True
	while temp > min_temp:
	    print('fitness best_sol')
	    print(best_sol)
	    print(fitness(matrix, best_sol))
	    if cambio:
	        fit = fitness(matrix, solution)

	    colores = list(set(solution))
	    new_solution = solution

	    # Vecino
	    nodo_cambio = np.random.choice(n)
	    colores.remove(solution[nodo_cambio])
	    color_cambio = np.random.choice(colores)
	    new_solution[nodo_cambio] = color_cambio
	    print('fitness best_sol 22222222222')
	    print(best_sol)
	    print(fitness(matrix, best_sol))
	    if counter > 3:
	    	return
	    else:
	    	counter += 1

	    # Cambio local
	    new_fit = fitness(matrix, new_solution)
	    if new_fit >= fit:
	        cambio = True
	        solution = new_solution
	        fit = new_fit
	        if new_fit > best_fit:  # Cambio global
	            best_sol = solution
	            best_fit = fit
	            print('Mejora Local!.')
	    else:
	        if np.random.random() <= np.math.exp((new_fit - fit) / temp):
	            cambio = True
	            solution = new_solution
	            fit = new_fit
	        else:
	            cambio = False
	    # Actualizar temp
	    del(new_solution)
	    del(new_fit)
	    temp *= alpha
	return(best_sol, best_fit)


def genGraph(N):
    ''' Genera un grafo de N nodos para probar el problema. '''
    M = np.random.randint(0, high=2, size=(N, N))
    for i in range(N):
        for j in range(i, N):
            if i == j:
                M[i, j] = 1
            else:
                M[i, j] = M[j, i]

    return(M)


def es_valida(matrix, solution):
    '''Checkea si un vector de colores es solución (válido).'''
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            if matrix[i, j] == 1:
                if solution[i] == solution[j]:
                    return(False)
    return(True)


grafo = genGraph(50)

sol, fit = main(grafo)