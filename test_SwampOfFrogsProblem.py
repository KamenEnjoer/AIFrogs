#2024-03-10 Nadežda Pyževskaja
'''
Yra nxn dydžio pelkė su r varlių kiekių.
Reikia padėti varles taip, kad tarp jų butu kuo didesnis atstumas.
'''

from collections import deque

class Node:
    def __init__(self, state): #Inicializacija kintamujų
        self.state = state

    def expand(self, problem): #Gražina visu prioretizuotu vietu pelkėje sąrašą
        return [Node(problem.result(self.state, action)) for action in problem.actions(self.state)]

def breadth_first_graph_search(problem): #Paieškos algoritmas
    node = Node(problem.initial)
    if problem.goal_test(node.state): #Ar nėra sprendimo iškart
        return node
    frontier = deque([node]) #Naujas pažistamų elementų sąrašas su node parametru
    explored = set() #Naujas ištirtu elementų sąrašas, tuščias
    while frontier:
        node = frontier.popleft() #Pajiemam pirmą elementą
        explored.add(tuple(map(tuple, node.state)))  #[[1, 2], [3, 4]] konvertuojame i ((1, 2), (3, 4)) ir idedam į istirtų elementų sąrašą
        for child in node.expand(problem): #Kol yra galimos vietos padėti varlę
            if tuple(map(tuple, child.state)) not in explored: #Jei elementas neištirtas
                if problem.goal_test(child.state): #tai tikriname, ar nebaigiasi varlės
                    return child
                frontier.append(child) #Jei ne, itraukiam elementą į pažistamu elementų sąrašo galą
                explored.add(tuple(map(tuple, child.state)))  #
    return None

class FrogsProblem:
    def __init__(self, n, r): #Inicializacija kintamujų
        self.n = n #pelkės dydis
        self.r = r #varlių kiekis
        self.initial = [[False] * n for _ in range(n)] #pelkės matrica

    def actions(self, state):#Paieška galimų varlėms vietų
        valid_actions = [] #tuščios aibės sukūrimas
        distance_map = [[0] * self.n for _ in range(self.n)]  #Distancijų žemėlapis (matrica)
        for i in range(self.n):
            for j in range(self.n): #Dvimatis foras
                if self.is_valid_position(state, i, j): #Jei i:j posicija laisva,
                    for x in range(self.n):
                        for y in range(self.n):  # Dvimatis foras
                            if state[x][y]: #Jei x:y stovi varlė
                                distance_map[i][j] += pow(abs(x-i) + abs(y-j), 0.5) #Sumuojame prie žemėlapio langelio distancijos ilgį. Kvadratinė šaknis reikalinga kad prioretizuoti langelius su atstumu nuo visų kitų varlių.
        ''' #for debug
        print("______________")
        for row in distance_map:
            print(" ".join(map(str, row)))
        #for debug '''
        max_distance = max(max(row) for row in distance_map) #gauname maksimalią distanciją
        for i in range(self.n):
            for j in range(self.n):  # Dvimatis foras
                if distance_map[i][j]==max_distance: #Jei žemėlapyje keli maksimalios distancijos
                    valid_actions.append((i, j)) #Visas prisijungiam prie galimų vietų aibės
        return valid_actions

    def result(self, state, action): #Varlės idėjimas
        new_state = [row[:] for row in state] #Nauja pelkės versija ant senos pagrindo
        new_state[action[0]][action[1]] = True #Padėjimas naujos varlės
        return new_state

    def is_valid_position(self, state, i, j): #Ar yra i:j pozicija laisva
        if not (0 <= i < self.n and 0 <= j < self.n): #Jei kintamieji išeina už lauko ribų
            return False #Atmetama
        if state[i][j]: #Ant pasirinktos vietos yra kita varlė
            return False #Atmetama
        return True

    def goal_test(self, state):#Ar visi varlės yra pelkėje
        return sum(row.count(True) for row in state) == self.r #Skaičiuojama valrių suma ir lyginama su paduotu pradžioje kiekių


problem = FrogsProblem(5, 5) #Problemos sukurimas, kur r<=n*n
solution = breadth_first_graph_search(problem) #Problemos sprendimas

if solution: #Jei sprendimas rastas
    print("Solution:")
    for row in solution.state: #Išvedama matrica, kur O tai varlės, o - tuščia vieta
        print(" ".join("O" if cell else "-" for cell in row))
else:
    print("Solution not found :(.") #Sprendimas nerastas
