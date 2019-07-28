import numpy as np
import itertools
import random
import matplotlib.pyplot as plt

# Die Funktion map_plot gibt den Plot der momentanen Verteilung der Personen im Raum aus.

def map_plot(Position_Map, Map, Iteration):
    hilf_wall = np.argwhere(Position_Map == 500)
    fig = plt.figure(figsize = (Position_Map.shape[1]/2, Position_Map.shape[0]/2))
    X_Axis = fig.add_subplot(111)
    Y_Axis = fig.add_subplot(111)
    X_Axis.set_xticks(np.arange(0.5, Position_Map.shape[1], 1))
    Y_Axis.set_yticks(np.arange(0.5, Position_Map.shape[0], 1))
    plt.xlim(0, Position_Map.shape[1]-1)
    plt.ylim(Position_Map.shape[0]-1, 0)
    plt.grid(axis = 'both')
    Y_Axis.scatter(np.where(Map == 3)[1], np.where(Map == 3)[0], marker = 's', s = 805,  c = 'blue')
    X_Axis.scatter(np.where(Position_Map == 1)[1], np.where(Position_Map == 1)[0], marker = 'o', s = 350, c = 'coral')
    Y_Axis.scatter(np.where(Position_Map == 500)[1], np.where(Position_Map == 500)[0], marker = 's', s = 805,  c = 'indigo')
    plt.savefig(str(Iteration))
    #plt.show()

# Die Funktion floor_field_plot gibt den Plot des Floorfields aus.

def floor_field_plot(FF, Iteration):
	z = FF.shape[0]
	s = FF.shape[1]
	plt.figure(figsize = (s/2, z/2))
	plt.imshow(FF, 'inferno', vmin = 0, vmax = max(FF[:,:][FF[:,:] < 500]+2), origin = 'upper', aspect = 'auto', interpolation = 'nearest')
	plt.colorbar()
	ax = plt.gca(); 
	# for i in range(s):
	#     for j in range(z):
	#         text = ax.text(j, i, FF[i, j], fontsize=12, horizontalalignment='left', verticalalignment='bottom', color="blue")  
	ax.set_xticks(np.arange(0, s, 1));
	ax.set_yticks(np.arange(0, z, 1));
	ax.set_xticklabels(np.arange(1, s+1, 1));
	ax.set_yticklabels(np.arange(1, z+1, 1));
	plt.savefig(str(Iteration+0.5))
	#plt.show()

# Die Funktion floor_field erhält die aus der Datei eingelesene Map sowie das aus map_data_generator
# generierte Array von Tueren und liefert das Floorfield zurück, das angibt wie weit jedes Feld vom
# Ausgang entfernt ist. Horizontale/vertikale Distanz ist 1 Einheit und Diagonale 1,5 Einheiten
# Die Funktion unterstützt Telportfelder

def floor_field(Map, Door, Climbable_Barriers):
    Floor_Field = Map.copy()
    Floor_Field[Floor_Field == 3] = 0
    for i in range(len(Door)):
        Floor_Field[Door[i][0], Door[i][1]] = 1
    neighbour_values = Door
    while not neighbour_values == []:
        new_neighbour_values = []
        for q in range(len(neighbour_values)):
            for i in range(3):
                for j in range(3):
                    if neighbour_values[q][0]+i-1 >= 0 and neighbour_values[q][1]+j-1 >= 0 and neighbour_values[q][0]+i-1 < Floor_Field.shape[0] and neighbour_values[q][1]+j-1 < Floor_Field.shape[1]:
                        slot = [neighbour_values[q][0]+i-1, neighbour_values[q][1]+j-1]
                        if [i, j] in [[1, 0], [0, 1], [2, 1], [1, 2]]:
                            if slot not in Climbable_Barriers:
                                if Floor_Field[slot[0], slot[1]] > Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 1 and Floor_Field[slot[0], slot[1]] < 500 or Floor_Field[slot[0], slot[1]] == 0:
                                    Floor_Field[slot[0], slot[1]] = Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 1
                                    new_neighbour_values.append([slot[0], slot[1]])
                                elif Floor_Field[slot[0], slot[1]] < 0:
                                    Teleports = np.where(Floor_Field == Floor_Field[slot[0], slot[1]])
                                    Floor_Field[Teleports[0][0], Teleports[1][0]] = Floor_Field[Teleports[0][1], Teleports[1][1]] = Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 1
                                    new_neighbour_values.append([Teleports[0][0], Teleports[1][0]])
                                    new_neighbour_values.append([Teleports[0][1], Teleports[1][1]])
                            else:
                                if Floor_Field[slot[0], slot[1]] > Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 2 and Floor_Field[slot[0], slot[1]] < 500 or Floor_Field[slot[0], slot[1]] == 0:
                                    Floor_Field[slot[0], slot[1]] = Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 2
                                    new_neighbour_values.append([slot[0], slot[1]])
                        else:
                            if slot not in Climbable_Barriers:
                                if Floor_Field[slot[0], slot[1]] == 0 or Floor_Field[slot[0], slot[1]] > Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 1.5 and Floor_Field[slot[0], slot[1]] < 500:
                                    Floor_Field[slot[0], slot[1]] = Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 1.5
                                    new_neighbour_values.append([slot[0], slot[1]])
                            else:
                                if Floor_Field[slot[0], slot[1]] == 0 or Floor_Field[slot[0], slot[1]] > Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 2.5 and Floor_Field[slot[0], slot[1]] < 500:
                                    Floor_Field[slot[0], slot[1]] = Floor_Field[neighbour_values[q][0], neighbour_values[q][1]] + 2.5
                                    new_neighbour_values.append([slot[0], slot[1]])
        new_neighbour_values.sort()
        neighbour_values = list(new_neighbour_values for new_neighbour_values,_ in itertools.groupby(new_neighbour_values)).copy()
    return Floor_Field

#Funktion die jeden Zeitschritt ein neues Floorfield zurückliefert basierend auf dem Original
#modifiziert um eine Konstante für Zellen in denen Personen stehten (bleiben)

def update_floorfield(Floor_Field, People_Not_Moving, Position_Map):
    FF = Floor_Field.copy()
    FF[Position_Map == 1] += 1
    for i in range(len(People_Not_Moving)):
        FF[People_Not_Moving[i][0], People_Not_Moving[i][1]] += 1
    return FF

# Die best_neighbour Funktion übernimmt die Koordinaten der betrachteten Person und das Floorfield und
# ermittelt das Nachbarfeld, das am nächsten am Ausgang dran ist. Wenn 2 Felder gleich gut sind, wird
# eines zufällig ausgewählt. Die Funktion unterstützt keine Randwerte, was aber bei genügend guter
# Konditionierung der Map unproblematisch ist. 

def best_neighbour(Coordinates, FF, Position_Map):
    Surrounding = FF[Coordinates[0]-1:Coordinates[0]+2, Coordinates[1]-1:Coordinates[1]+2]
    Lowest_Neighbour = np.where(Surrounding == np.amin(Surrounding))
    if len(Lowest_Neighbour[0]) == 1:
        Target = [int(Lowest_Neighbour[0]) - 1 + Coordinates[0], int(Lowest_Neighbour[1]) - 1 + Coordinates[1]]
        if Position_Map[Target[0], Target[1]] == 0 and Position_Map[int(Lowest_Neighbour[0]) - 1 + Target[0], int(Lowest_Neighbour[1]) - 1 + Target[1]] != 500:
            return [Target[0], Target[1], int(Lowest_Neighbour[0]) - 1 + Target[0], int(Lowest_Neighbour[1]) - 1 + Target[1]]
        else:
            return [Target[0], Target[1], 0, 0]
    else:
        Choice = random.randint(0, len(Lowest_Neighbour[0])-1)
        Target = [int(Lowest_Neighbour[0][Choice]) - 1 + Coordinates[0], int(Lowest_Neighbour[1][Choice]) - 1 + Coordinates[1]]
        if Position_Map[Target[0], Target[1]] == 0 and Position_Map[int(Lowest_Neighbour[0][Choice]) - 1 + Target[0], int(Lowest_Neighbour[1][Choice]) - 1 + Target[1]] != 500:
            return [Target[0], Target[1], int(Lowest_Neighbour[0][Choice]) - 1 + Target[0], int(Lowest_Neighbour[1][Choice]) - 1 + Target[1]]
        else:
            return [Target[0], Target[1], 0, 0]

# Die Funktion map_data_generator erhaelt die Karte, die aus der Datei eingelesen wird, als Eingabe und
# gibt alle für uns relevanten Parameter und Daten der Map wieder. Explizit sind dies:
# Die Position_Map, die letzten Endes ausgegeben und angezeigt wird,
# Das Floor_Field ueber das die Personen navigieren,
# Das Array Teleport_Memory in dem sich alle Teleporter koordinaten in Paaren befinden und
# People als Array der Personen-Koordinaten auf dem Feld
# Diese Funktionen wurden ausgelagert um die Funktion time_loop uebersichtlicher zu gestalten

def map_data_generator(Map):
    Position_Map = Map.copy()
    Climbable_Barriers_Memory = np.where(Position_Map == 3)
    Position_Map[Position_Map == 3] = 0
    Climbable_Barriers = []
    for i in range(len(Climbable_Barriers_Memory[0])):
        Climbable_Barriers.append([Climbable_Barriers_Memory[0][i], Climbable_Barriers_Memory[1][i]])
    People = []
    People_Memory = np.where(Position_Map == 1)
    for i in range(len(People_Memory[0])):
        People.append([People_Memory[0][i], People_Memory[1][i]])
    Teleport_Memory = []
    for i in range(int(len(np.where(Position_Map < 0)[0])/2)):
        Teleport_i = np.where(Position_Map == -(i+1))
        Teleport_Memory.extend(([Teleport_i[0][0], Teleport_i[1][0]], [Teleport_i[0][1], Teleport_i[1][1]]))
    Door = []
    Door_Memory = np.where(Position_Map == 2)
    for i in range(len(Door_Memory[0])):
        Door.append([Door_Memory[0][i], Door_Memory[1][i]])
    FF_Base = Position_Map.copy()
    FF_Base[FF_Base == 1] = 0
    Floor_Field = floor_field(FF_Base, Door, Climbable_Barriers)
    Position_Map[Position_Map < 0] = 0
    Position_Map[Position_Map == 2] = 0
    return Position_Map, Floor_Field, Door, Teleport_Memory, People, Climbable_Barriers

# Die Funktion random_pedestrians übernimmt eine Karte und besetzt sie mit einer zufälligen Anzahl von
# Personen an zufälligen Stellen und gibt diese mti Menschen gefülte Map wieder.

def random_pedestrians(Map):
    RandPed = Map.copy()
    pedestrians = random.randint(3, 10)
    nzeilen = Map.shape[0]     
    nspalten = Map.shape[1]
    while True:
        a = random.randint(0, nzeilen-1)
        b = random.randint(0,nspalten-1)  
        if RandPed[a,b] == 0:
            RandPed[a,b] = RandPed[a,b] + 1
        if (RandPed.sum() - Map.sum())/1 == pedestrians:
            break
    return RandPed

# Die Funktion time_loop simuliert die eigentliche Evakuierung basierend auf der Map und einer Panik(Wahrscheinlichkeit)
# Sie gibt die Anzahl der benötigten Zeitschritte zur Vollständigen Evakuierung aus. Die Funktion unterstützt Telportfelder.

def time_loop(Map, Panic):
    Position_Map, Floor_Field_Original, Door, Teleport_Memory, People, Climbable_Barriers = map_data_generator(Map)
    Floor_Field = Floor_Field_Original.copy()
    #floor_field_plot(Floor_Field)
    Climbing = []
    Iterations = 0
    #map_plot(Position_Map, Iterations)
    while len(People) != 0:
        Players = []
        People_New = []
        People_Teleport = []
        People_Not_Moving = []
        for i in range(len(People)):
            if random.randint(1, 100) > Panic:
                if [People[i][0], People[i][1]] in Climbing:
                    People_Not_Moving.append([People[i][0], People[i][1]])
                    Climbing.remove([People[i][0], People[i][1]])
                else:
                    Players.append([[People[i][0], People[i][1]], best_neighbour([People[i][0], People[i][1]], Floor_Field, Position_Map)])
            else:
                People_Not_Moving.append([People[i][0], People[i][1]])
        random.shuffle(Players)
        X = True
        while X:
            A = 0
            for i in range(len(Players)):
                if Position_Map[Players[i-A][1][0], Players[i-A][1][1]] == 0:
                    if [Players[i-A][1][0], Players[i-A][1][1]] in Climbable_Barriers:
                            Climbing.append([Players[i-A][1][0], Players[i-A][1][1]])
                            #People_Not_Moving.append([Players[i-A][1][0], Players[i-A][1][1]])
                    if Map[Players[i-A][1][0], Players[i-A][1][1]] >= 0:
                        Position_Map[Players[i-A][0][0], Players[i-A][0][1]] = 0
                        Position_Map[Players[i-A][1][0], Players[i-A][1][1]] = 1
                        if Players[i-A][1][2] != 0 and Position_Map[Players[i-A][1][2], Players[i-A][1][3]] == 0 and [Players[i-A][1][0], Players[i-A][1][1]] not in Climbable_Barriers and [Players[i-A][1][2], Players[i-A][1][3]] not in Climbable_Barriers:
                        	Position_Map[Players[i-A][1][0], Players[i-A][1][1]] = 0
                        	Position_Map[Players[i-A][1][2], Players[i-A][1][3]] = 1
                        del Players[i-A]
                        A += 1
                    else:
                        index = Teleport_Memory.index([Players[i-A][1][0], Players[i-A][1][1]])
                        index_shift = index % 2
                        if Position_Map[Teleport_Memory[index - index_shift][0], Teleport_Memory[index - index_shift][1]] == 0:
                            Position_Map[Players[i-A][0][0], Players[i-A][0][1]] = 0
                            Position_Map[Players[i-A][1][0], Players[i-A][1][1]] = 1
                            People_Teleport.append([Players[i-A][1][0], Players[i-A][1][1]])
                            del Players[i-A]
                            A += 1
            if A == 0:
                X = False
        for i in range(len(Players)):
            People_Not_Moving.append([Players[i][0][0], Players[i][0][1]])
        for i in range(len(Door)):
            Position_Map[Door[i][0], Door[i][1]] = 0
        for i in range(len(People_Teleport)):
            Telport_ID = Map[People_Teleport[i][0], People_Teleport[i][1]]
            Position_Map[Map == Telport_ID] = 1
            Position_Map[People_Teleport[i][0], People_Teleport[i][1]] = 0
        People_New = np.argwhere(Position_Map == 1)
        Iterations += 1
        map_plot(Position_Map, Map, Iterations)
        #print()
        #print(Position_Map)
        People = People_New
        floor_field_plot(Floor_Field, Iterations)
        Floor_Field = update_floorfield(Floor_Field_Original, People_Not_Moving, Position_Map)
    return Iterations

Room = np.loadtxt('Supermarkt_Voll.txt')
print(time_loop(Room, 5))
