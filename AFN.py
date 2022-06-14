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
                    possibleTransitions += epsilon
    
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

        print(f'{currentState} --------------- {w[i]}')
        nextState = findPossibleTransitions(currentState, w[i], transitions)

        if nextState is None:
            print("Essa cadeia não é aceita")
            #return False

        elif type(nextState) is list:
            while True:
                aux = path.copy()
                aux.append(nextState.pop())
                currentState = aux[-1]
                allPaths.append(aux)

                if not nextState:
                    break
        else:
            currentState = nextState
            path.append(currentState)
            
        print(arrow)
        time.sleep(1)
    
    path.append(currentState)
    print(currentState)

    print(f'\nPath {path}')

    allPaths.append(path)

    #Check if all of the paths are in their max reach
    for i in range(len(allPaths)):
        index = len(allPaths[i]) - 1
        if index < len(w):
            possible = findPossibleTransitions(allPaths[i][index], w[index], transitions)
            if type(possible) is list:
                while True:
                    aux = allPaths[i].copy()
                    #p has to be removed
                    if len(possible) == 1:
                        print(f'Removing {allPaths[i]}\n')
                        allPaths.remove(allPaths[i])
                        
                    aux.append(possible.pop())
                    print(f'\nAppending to allPaths {aux}\n')
                    allPaths.append(aux)

                    if not possible:
                        break

            elif possible:
                print(f'\nAppending to allPaths {possible}\n')
                allPaths[i].append(possible)

    #qo, q1, q1 nao esta no seu maximo, então tem q checar com a ultima letra do alfabeto pra ver para onde mais ele pode ir

    print(f'\nAll Paths {allPaths}')

    #TODO
    # remove copys?

    if currentState not in finalStates:
        return False

    return True

def afn(filename):
    alphabet, states, initialState, finalStates, transitions = ir.readInputs(filename)

    w = list(input("Insira a cadeia de entrada: "))

    #Error check in the input string
    for char in w:
        if char not in alphabet:
            print("Cadeia de entrada inválida")
            sys.exit()
    
    result = processment(initialState, w, transitions, finalStates)

    if result:
        print("\nSucesso")
    else:
        print("\nEssa cadeia não foi aceita pelo autômato")

afn("teste.txt")