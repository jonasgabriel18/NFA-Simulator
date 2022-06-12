import Input_Reader as ir
import threading
import time
import sys
    

def findTransition(state, char, transitions):
    a=[]
    for s in state:
        #print(f"{state}, {char}, {transitions}")
        for transition in transitions:
            #if transition[2]=="epsilon":
                #print("EPSILON")
            if s == transition[0]:
                if char == transition[2]:
                    a.append(transition[1])
                    epsilon=findTransition([transition[1]], 'epsilon', transitions)
                    if epsilon!=None:
                        print(f"E {epsilon}")
                        a+=epsilon
                    print(a)
                elif char!=transition[2] and s==transition[0]:
                    if char!='epsilon':
                        print("Morreu")
        
    if a!=[]:
        return a
    return None



def processment(initialState, w, transitions, finalStates):
    arrow = u'\u2193'
    aceito=False
    currentState = [initialState]
    print(finalStates)
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

    for elemento in currentState:

        #if elemento not in finalStates:
        print(elemento)
        aceito=aceito or (elemento in finalStates)
        #print(f"STATUS DO ACEITO: {aceito}")

    return aceito

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

#alfabeto, estados, ei, ef, transicoes=I_R.readInputs(teste)

#def worker(#um estado
#):
#    for i in range(#quantidade de transicoes desse estado
#    ):
        #criar threads nessa quantidade de transicoes, sendo uma thread para cada possibilidade 