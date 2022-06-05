import Input_Reader as ir
import time
import sys

def findTransition(state, char, transitions):
    for transition in transitions:
        if state == transition[0] and char == transition[2]:
            return transition[1]
    
    return None

def processment(initialState, w, transitions, finalStates):
    arrow = u'\u2193'

    currentState = initialState

    for i in range(len(w)):
        print(f'{currentState} --------------- {w[i]}')
        nextState = findTransition(currentState, w[i], transitions)
        if nextState is None:
            print("Essa cadeia não é aceita")
            sys.exit()
        else:
            currentState = nextState

        print(arrow)
        time.sleep(1)

    print(currentState)

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