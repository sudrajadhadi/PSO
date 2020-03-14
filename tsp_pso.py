# encoding:utf-8
from operator import attrgetter
import random, sys, time, copy

class Graph:

	def __init__(self, amount_vertices):
		self.edges = {}
		self.vertices = set() 
		self.amount_vertices = amount_vertices 

	def addEdge(self, src, dest, cost = 0):
		# checks if the edge already exists
		if not self.existsEdge(src, dest):
			self.edges[(src, dest)] = cost
			self.vertices.add(src)
			self.vertices.add(dest)

	def existsEdge(self, src, dest):
		return (True if (src, dest) in self.edges else False)

	def showGraph(self):
		print('Showing the graph:\n')
		for edge in self.edges:
			print('%d linked in %d with cost %d' % (edge[0], edge[1], self.edges[edge]))

	def getCostPath(self, path):
		
		total_cost = 0
		for i in range(self.amount_vertices - 1):
			total_cost += self.edges[(path[i], path[i+1])]

		total_cost += self.edges[(path[self.amount_vertices - 1], path[0])]
		return total_cost


	def getRandomPaths(self, max_size):

		random_paths, list_vertices = [], list(self.vertices)

		initial_vertice = random.choice(list_vertices)
		if initial_vertice not in list_vertices:
			print('Error: initial vertice %d not exists!' % initial_vertice)
			sys.exit(1)

		list_vertices.remove(initial_vertice)
		list_vertices.insert(0, initial_vertice)

		for i in range(max_size):
			list_temp = list_vertices[1:]
			random.shuffle(list_temp)
			list_temp.insert(0, initial_vertice)

			if list_temp not in random_paths:
				random_paths.append(list_temp)

		return random_paths

class CompleteGraph(Graph):

	def generates(self):
		for i in range(self.amount_vertices):
			for j in range(self.amount_vertices):
				if i != j:
					weight = random.randint(1, 10)
					self.addEdge(i, j, weight)

class Particle:

	def __init__(self, solution, cost):
		self.solution = solution
		self.pbest = solution
		self.cost_current_solution = cost
		self.cost_pbest_solution = cost
		self.velocity = []

	def setPBest(self, new_pbest):
		self.pbest = new_pbest
	
	def getPBest(self):
		return self.pbest

	def setVelocity(self, new_velocity):
		self.velocity = new_velocity

	def getVelocity(self):
		return self.velocity

	def setCurrentSolution(self, solution):
		self.solution = solution

	def getCurrentSolution(self):
		return self.solution

	def setCostPBest(self, cost):
		self.cost_pbest_solution = cost

	def getCostPBest(self):
		return self.cost_pbest_solution

	def setCostCurrentSolution(self, cost):
		self.cost_current_solution = cost

	def getCostCurrentSolution(self):
		return self.cost_current_solution

	def clearVelocity(self):
		del self.velocity[:]


class PSO:

	def __init__(self, graph, iterations, size_population, beta=1, alfa=1):
		self.graph = graph 
		self.iterations = iterations
		self.size_population = size_population
		self.particles = [] 
		self.beta = beta
		self.alfa = alfa
		solutions = self.graph.getRandomPaths(self.size_population)

		if not solutions:
			print('Initial population empty! Try run the algorithm again...')
			sys.exit(1)

		for solution in solutions:
			particle = Particle(solution=solution, cost=graph.getCostPath(solution))
			self.particles.append(particle)

		self.size_population = len(self.particles)


	def setGBest(self, new_gbest):
		self.gbest = new_gbest

	def getGBest(self):
		return self.gbest

	def run(self):

		for t in range(self.iterations):

			self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

			for particle in self.particles:

				particle.clearVelocity()
				temp_velocity = []
				solution_gbest = copy.copy(self.gbest.getPBest()) 
				solution_pbest = particle.getPBest()[:]
				solution_particle = particle.getCurrentSolution()[:]
				
				for i in range(self.graph.amount_vertices):
					if solution_particle[i] != solution_pbest[i]:
						swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

						temp_velocity.append(swap_operator)

						aux = solution_pbest[swap_operator[0]]
						solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
						solution_pbest[swap_operator[1]] = aux

				for i in range(self.graph.amount_vertices):
					if solution_particle[i] != solution_gbest[i]:
						swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

						temp_velocity.append(swap_operator)

						aux = solution_gbest[swap_operator[0]]
						solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
						solution_gbest[swap_operator[1]] = aux

				
				particle.setVelocity(temp_velocity)

				for swap_operator in temp_velocity:
					if random.random() <= swap_operator[2]:
						aux = solution_particle[swap_operator[0]]
						solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
						solution_particle[swap_operator[1]] = aux
				
				particle.setCurrentSolution(solution_particle)
				cost_current_solution = self.graph.getCostPath(solution_particle)
				particle.setCostCurrentSolution(cost_current_solution)

				if cost_current_solution < particle.getCostPBest():
					particle.setPBest(solution_particle)
					particle.setCostPBest(cost_current_solution)
		

if __name__ == "__main__":
	
	graph = Graph(amount_vertices=5)

	graph.addEdge(0, 1, 1)
	graph.addEdge(1, 0, 1)
	graph.addEdge(0, 2, 3)
	graph.addEdge(2, 0, 3)
	graph.addEdge(0, 3, 4)
	graph.addEdge(3, 0, 4)
	graph.addEdge(0, 4, 5)
	graph.addEdge(4, 0, 5)
	graph.addEdge(1, 2, 1)
	graph.addEdge(2, 1, 1)
	graph.addEdge(1, 3, 4)
	graph.addEdge(3, 1, 4)
	graph.addEdge(1, 4, 8)
	graph.addEdge(4, 1, 8)
	graph.addEdge(2, 3, 5)
	graph.addEdge(3, 2, 5)
	graph.addEdge(2, 4, 1)
	graph.addEdge(4, 2, 1)
	graph.addEdge(3, 4, 2)
	graph.addEdge(4, 3, 2)

	pso = PSO(graph, iterations=100, size_population=10, beta=1, alfa=0.9)
	pso.run() # runs the PSO algorithm

	print('gbest: %s | cost: %d\n' % (pso.getGBest().getPBest(), pso.getGBest().getCostPBest()))
