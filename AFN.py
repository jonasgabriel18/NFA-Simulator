import Input_Reader as ir
import time
import sys
    
def findPossibleTransitions(state, char, transitions):
    possibleTransitions = [] #antigo 'a'

    for transition in transitions:
        if state == transition[0] and char == transition[2]:
            possibleTransitions.append(transition[1])
            epsilon = findPossibleTransitions(transition[1], 'epsilon', transitions)
            if epsilon != None:
                    #print(f'epsilon = {epsilon}\n')
                    possibleTransitions.append(epsilon)
                    #print(f'possible transitions apos soma = {possibleTransitions}\n')
    
    if possibleTransitions:
        if len(possibleTransitions) == 1:
            return possibleTransitions[0]
        else:
            return possibleTransitions

    return None

def processment(initialState, w, transitions, finalStates):
    arrow = u'\u2193'
  
    allPaths = list()
    path = list()
    path.append(initialState)
    currentState = initialState

    for i in range(len(w)):

        nextState = findPossibleTransitions(currentState, w[i], transitions)
        #print(f'nextState = {nextState}\n')
        if type(nextState) is list:
            while True:
                aux = path.copy()
                #print(f'next state = {nextState}\n')
                aux.append(nextState.pop())
                #print(f'aux = {aux}\n')
                currentState = aux[-1]
                #print(f'current state = {currentState}\n')
                allPaths.append(aux)

                if not nextState:
                    break
        elif nextState:
            currentState = nextState
            path.append(currentState)
            
    
    path.append(currentState)

    allPaths.append(path)

    #Check if all of the paths are in their max reach
    for i in range(len(allPaths)):
        index = len(allPaths[i]) - 1 #currently it only checks the last letter
        if index < len(w):
            possible = findPossibleTransitions(allPaths[i][index], w[index], transitions)
            if type(possible) is list:
                while True:
                    aux = allPaths[i].copy()
                    #p has to be removed
                    if len(possible) == 1:
                        allPaths.remove(allPaths[i])

                    aux.append(possible.pop())
                    allPaths.append(aux)

                    if not possible:
                        break

            elif possible:
                allPaths[i].append(possible)

    #qo, q1, q1 nao esta no seu maximo, então tem q checar com a ultima letra do alfabeto pra ver para onde mais ele pode ir

    if allPaths:
        return allPaths

    return None

def printPaths(allPaths, w, finalStates):
    arrow = u'\u2193' #unicode downwards arrow symbol
    count = 1
    process_time = time.time()

    for path in allPaths:
        if len(path) == len(w):
            print('===================================================')
            print(f'Starting process {count}')
            print('===================================================\n')

            for i in range(len(w)):
                print(f'{path[i]} --------------- {w[i]}')
                print(arrow)
                time.sleep(1)

            print(path[-1])
            if path[-1] not in finalStates:
                print('\nThis process is not accepted by the NFA\n')
            else:
                print('\nThis process is accepted by the NFA\n')
        
            count += 1
        elif len(path) < len(w):
            print('===================================================')
            print(f'Starting process {count}')
            print('===================================================\n')

            for i in range(len(path)):
                print(f'{path[i]} --------------- {w[i]}')
                print(arrow)
                time.sleep(1)

            print(path[-1])
            if path[-1] not in finalStates:
                print('\nThis process is not accepted by the NFA\n')
            else:
                print('\nThis process is accepted by the NFA\n')
        
            count += 1

    

    print(f'\nFinished processing. It took {time.time() - process_time} seconds\n')

def afn(filename):
    alphabet, states, initialState, finalStates, transitions = ir.readInputs(filename)

    w = list(input("Insira a cadeia de entrada: "))

    #Error check in the input string
    for char in w:
        if char not in alphabet:
            print("Cadeia de entrada inválida")
            sys.exit()
    
    processment_result = processment(initialState, w, transitions, finalStates)
    printPaths(processment_result, w, finalStates)

afn("teste.txt")