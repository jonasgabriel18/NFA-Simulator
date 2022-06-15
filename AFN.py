import Input_Reader as ir
import time
import sys

#TODO
#pequeno bug em que, por exemplo, há dois caminhos corretos, um na vdd é mais correto
    
def findPossibleTransitions(state, char, transitions):
    possibleTransitions = [] #antigo 'a'

    for transition in transitions:
        if state == transition[0] and char == transition[2]:
            possibleTransitions.append(transition[1])
            epsilon = findPossibleTransitions(transition[1], 'epsilon', transitions)
            if epsilon:
                    if type(epsilon) is list:
                        while epsilon:
                            possibleTransitions.append(epsilon.pop(0))
                    else:
                        possibleTransitions.append(epsilon)

    
    if possibleTransitions:
        if len(possibleTransitions) == 1:
            return possibleTransitions[0]
        else:
            return possibleTransitions

    return None

def findOtherInitialStates(initialState, transitions):
    initialStates = list()
    initialStates.append(initialState)
    aux = initialState

    while True:
        epsilon_ini = findPossibleTransitions(aux, 'epsilon', transitions)
        
        if epsilon_ini is None:
            break

        if type(epsilon_ini) is list:
            while epsilon_ini:
                initialStates.append(epsilon_ini.pop(0))
        else:
            initialStates.append(epsilon_ini)

        aux = [epsilon_ini]
        
    return initialStates


def processment(initialState, w, transitions, finalStates):
  
    allPaths = list()
    path = list()
   
    inStates = findOtherInitialStates(initialState, transitions)
    #print(inStates)

    while inStates:
        path.clear()
        currentState = inStates.pop(0)
        path.append(currentState)
        
        for i in range(len(w)):
            nextState = findPossibleTransitions(currentState, w[i], transitions)

            if type(nextState) is list:
                while True:
                    aux = path.copy() #TODO maybe the path needs to be removed as well 
                    aux.append(nextState.pop())
                    currentState = aux[-1]
                    allPaths.append(aux)

                    if not nextState:
                        break

            elif nextState:
                currentState = nextState
                path.append(currentState)
            else:
                break
                
        #path.append(currentState)
        allPaths.append(path)


    #Check if all of the paths are in their max reach
    for i in range(len(allPaths)):
        while len(allPaths[i]) <= len(w):
            index = len(allPaths[i]) - 1 #currently it only checks the last letter
            possible = findPossibleTransitions(allPaths[i][index], w[index], transitions)
            #print(f'Possible = {possible}\nIndex = {index}\n')
            #print(allPaths[i])
            if type(possible) is list:
                while True:
                    aux = allPaths[i].copy()
                    #p has to be removed
                    if len(possible) == 1:
                        allPaths.remove(allPaths[i])
                        
                    aux.append(possible.pop())
                    allPaths.append(aux)
                    #print(f'Path appended hamina hamina {aux}\n')

                    if not possible:
                        break

            elif possible:
                allPaths[i].append(possible)
            else:
                break
    

    #it was noticed that some of the paths were on their max-1 reach, so is necessary to repeat the process for some of the paths

    for i in range(len(allPaths)):
        if len(allPaths[i]) >= len(w):
            lastReach = findPossibleTransitions(allPaths[i][-1], w[-1], transitions)
            if type(lastReach) is list:
                while True:
                    aux = allPaths[i].copy()
                    aux.append(lastReach.pop(0))
                    allPaths.append(aux)

                    if not lastReach:
                        break
            elif lastReach:
                allPaths[i].append(lastReach)
            else:
                break

    if allPaths:
        return allPaths

    return None

def dropDuplicates(allPaths):
    aux = []
    for i in range(len(allPaths)):
        if allPaths[i] not in aux:
            aux.append(allPaths[i])
    return aux

def printPaths(allPaths, w, finalStates):
    arrow = u'\u2193' #unicode downwards arrow symbol
    process_counter = 1
    process_time = time.time()
    isAccepted = False

    allPaths = dropDuplicates(allPaths)

    for path in allPaths:
        print('===================================================')
        print(f'\tStarting process {process_counter}')
        print('===================================================\n')

        if len(path) >= len(w):
            for i in range(len(w)):
                print(f'\t{path[i]} --------------- {w[i]}')
                print(f'\t{arrow}')
                time.sleep(0.8)

            if path[-1] not in finalStates:
                print('\t' + path[-1])
                print(f'\t{arrow}')
                print('\tX')
                print('\nThis process is not accepted by the NFA\n')
            else:
                print('\t' + path[-1])
                print('\nThis process is accepted by the NFA\n')
                isAccepted = True
        
        elif len(path) < len(w):
            for i in range(len(path)):
                print(f'\t{path[i]} --------------- {w[i]}')
                print(f'\t{arrow}')
                time.sleep(0.8)

            print('\tX')
            print('\nThis process is not accepted by the NFA\n')
        
        process_counter += 1

    print(f'\nFinished processing. It took {time.time() - process_time} seconds\n')

    return isAccepted

def afn(filename):
    alphabet, states, initialState, finalStates, transitions = ir.readInputs(filename)

    w = list(input("Insira a cadeia de entrada: "))

    #Error check in the input string
    for char in w:
        if char not in alphabet:
            print("Cadeia de entrada inválida")
            sys.exit()
    
    processment_result = processment(initialState, w, transitions, finalStates)

    if printPaths(processment_result, w, finalStates):
        print('\033[1;32mCadeia aceita pelo automato!\n')
    else:
        print('\033[1;31mCadeia negada pelo automato!\n')

afn("teste.txt")

#Examplos testados:
    # Slides 2 de AFN:
        # 5 
        # 4
        # exercicio p entrega