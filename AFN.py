import Input_Reader as ir
import time
import sys
    
def findPossibleTransitions(state, char, transitions):
    possibleTransitions = [] #antigo 'a'

    for transition in transitions:
        if state == transition[0] and char == transition[2]:
            #print('append')
            possibleTransitions.append(transition[1])
            #epsilon = findPossibleTransitions(transition[1], 'epsilon', transitions)
            #if epsilon != None:
                    #possibleTransitions += epsilon
    
    #print(f'Possible transitions {possibleTransitions}')

    if possibleTransitions:
        if len(possibleTransitions) == 1:
            return possibleTransitions[0]
        else:
            return possibleTransitions

    return None

def processment(initialState, w, transitions, finalStates):
    arrow = u'\u2193'
    moreWays = False
    allPaths = list()
    theWays = list()
    
    while True:
        path = list()
        path.append(initialState)
        currentState = initialState
        for i in range(len(w)):
            print(f'{currentState} --------------- {w[i]}')
            nextState = findPossibleTransitions(currentState, w[i], transitions)
            if nextState is None:
                print("Essa cadeia não é aceita")
                #moreWays = False
                #return False
            elif type(nextState) is list:

                if moreWays:
                    moreWays = False
                else:
                    moreWays = True

                if len(theWays) == 0:
                    theWays = nextState.copy()
                    currentState = theWays.pop(0)

                if len(theWays) == 0:
                    theWays.clear()
                    moreWays = False

                path.append(currentState)
            else:
                currentState = nextState
                path.append(currentState)
                moreWays = False

            print(arrow)
            time.sleep(1)
        
        print(currentState)

        print(f'\nPath {path}')

        allPaths.append(path)

        if not moreWays:
            break


    # TODO
    # Ok, na teoria, esta função deve retornar o all paths, e outra deve ser responsavel por printar
    # farei isso depois.
    # implementar transicoes epsilon (vamo meu jocat)
    # a dinamica se houver mais de um estado inicial deve ser diferente também.

    print(f'\nAll Paths {allPaths}')

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