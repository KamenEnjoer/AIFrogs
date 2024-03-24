#2024-03-10 Nadezda Pyzevskaja
'''
Yra nxn dydzio pelke su r varliu kiekiu.
Reikia padeti varles taip, kad tarp ju butu kuo didesnis atstumas.
'''

from collections import deque

class Node:
    def __init__(self, state): #Inicializacija kintamuju
        self.state = state

    def expand(self, problem): #Grazina visu prioretizuotu vietu pelkeje sarasa
        return [Node(problem.result(self.state, action)) for action in problem.actions(self.state)]

def breadth_first_graph_search(problem): #Paieskos algoritmas
    node = Node(problem.initial)
    if problem.goal_test(node.state): #Ar nera sprendimo iskart
        return node
    frontier = deque([node]) #Naujas pazistamu elementu sarasas su node parametru
    explored = set() #Naujas istirtu elementu sarasas, tuscias
    while frontier:
        node = frontier.popleft() #Pajiemam pirma elementa
        explored.add(tuple(map(tuple, node.state)))  #[[1, 2], [3, 4]] konvertuojame i ((1, 2), (3, 4)) ir idedam i istirtu elementu sarasa
        for child in node.expand(problem): #Kol yra galimos vietos padeti varle
            if tuple(map(tuple, child.state)) not in explored: #Jei elementas neistirtas
                if problem.goal_test(child.state): #tai tikriname, ar nebaigiasi varles
                    return child
                frontier.append(child) #Jei ne, itraukiam elementa i pazistamu elementu saraso gala
                explored.add(tuple(map(tuple, child.state)))  #
    return None

class FrogsProblem:
    def __init__(self, n, r): #Inicializacija kintamuju
        self.n = n #pelkes dydis
        self.r = r #varliu kiekis
        self.initial = [[False] * n for _ in range(n)] #pelkes matrica

    def actions(self, state):#Paieska galimu varlems vietu
        valid_actions = [] #tuscios aibes sukurimas
        distance_map = [[0] * self.n for _ in range(self.n)]  #Distanciju zemelapis (matrica)
        for i in range(self.n):
            for j in range(self.n): #Dvimatis foras
                if self.is_valid_position(state, i, j): #Jei i:j posicija laisva,
                    for x in range(self.n):
                        for y in range(self.n):  # Dvimatis foras
                            if state[x][y]: #Jei x:y stovi varle
                                distance_map[i][j] += pow(abs(x-i) + abs(y-j), 0.5) #Sumuojame prie zemelapio langelio distancijos ilgi. Kvadratinė šaknis reikalinga kad prioretizuoti langelius su atstumu nuo visu kitu varliu.
        ''' #for debug
        print("______________")
        for row in distance_map:
            print(" ".join(map(str, row)))
        #for debug '''
        max_distance = max(max(row) for row in distance_map) #gauname maksimalia distancija
        for i in range(self.n):
            for j in range(self.n):  # Dvimatis foras
                if distance_map[i][j]==max_distance: #Jei zemelapyje keli maksimalios distancijos
                    valid_actions.append((i, j)) #Visas prisijungiam prie galimu vietu aibes
        return valid_actions

    def result(self, state, action): #Varles idejimas
        new_state = [row[:] for row in state] #Nauja pelkes versija ant senos pagrindo
        new_state[action[0]][action[1]] = True #Pridejimas naujos varles
        return new_state

    def is_valid_position(self, state, i, j): #Ar yra i:j pozocoja laisva
        if not (0 <= i < self.n and 0 <= j < self.n): #Jei kintamieji iseina uz lauko ribu
            return False #Atmetama
        if state[i][j]: #Ant pasirinktos vietos yra kita varle
            return False #Atmetama
        return True

    def goal_test(self, state):#Ar visi varles yra pelkeje
        return sum(row.count(True) for row in state) == self.r #Skaiciuojama valriu suma ir liginama su paduotu pradzioje kiekiu


problem = FrogsProblem(5, 5) #Problemos sukurimas, kur r<=n*n
solution = breadth_first_graph_search(problem) #Problemos sprendimas

if solution: #Jei sprendimas rastas
    print("Solution:")
    for row in solution.state: #Isvedama matrica, kur O tai varles, o - tuscia vieta
        print(" ".join("O" if cell else "-" for cell in row))
else:
    print("Solution not found :(.") #Sprendimas nerastas
