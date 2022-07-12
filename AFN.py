import Input_Reader as ir
import time
import sys

# findPossibleTransitions() busca os estados para onde se pode ir levando em conta o caractere lido pelo automâto e o estado atual.
# A função também busca transições com a cadeia vazia (epsilon) via uso de recursão
#
# @Params:
#   state: estado atual do automâto
#   char: caractere lido pelo automâto
#   transitions: todas as transições do automâto
#
# Retorna:
#   apenas um se estado se ele for o único encontrado;
#   uma lista de estados possíveis de se ir, tendo em vista o não-determinismo
#   None se não for encontrado nenhum caminho
#  

def findPossibleTransitions(state, char, transitions):
    possibleTransitions = []

    for transition in transitions:
        if state == transition[0] and char == transition[2]:
            possibleTransitions.append(transition[1])
            epsilonTransitions = findPossibleTransitions(transition[1], 'epsilon', transitions)
            if epsilonTransitions:
                    if type(epsilonTransitions) is list:
                        while epsilonTransitions:
                            possibleTransitions.append(epsilonTransitions.pop(0))
                    else:
                        possibleTransitions.append(epsilonTransitions)

    if possibleTransitions:
        if len(possibleTransitions) == 1:
            return possibleTransitions[0]
        else:
            return possibleTransitions

    return None

# findOtherInitialStates() busca saber se é possível começar em outro estado graças a alguma transição epsilon.
#
# Params():
#   initialState: estado inicial do automâto
#   transitions: todas as transições do automâto
#
# Retorna:
#   se não foi encontrado nenhuma transição epsilon partindo do estado inicial, retorna o próprio estado inicial,
#   caso contrário, retorna uma lista com os estados em que o automâto pode começar.

def findOtherInitialStates(initialState, transitions):
    possibleInitialStates = list()
    possibleInitialStates.append(initialState)
    aux = initialState

    while True:
        epsilon_ini = findPossibleTransitions(aux, 'epsilon', transitions)
        
        if epsilon_ini is None:
            break

        if type(epsilon_ini) is list:
            while epsilon_ini:
                possibleInitialStates.append(epsilon_ini.pop(0))
        else:
            possibleInitialStates.append(epsilon_ini)

        aux = [epsilon_ini]
        
    return possibleInitialStates

# processment() é a função que gera todas as sequências de processamento do automâto para a devida cadeia de entrada
#
# @Params:
#   initialState: estado inicial do automâto
#   w: cadeia de entrada
#   transitions: todas as transições do automâto
#
# Retorna:
#   allPaths: uma lista de lista que contém todos os processamentos
#   pode retornar None caso não há nenhum caminho possível
#

def processment(initialState, w, transitions):
  
    allPaths = list()
    path = list() #lista de guarda o caminho atual seguido pelo automâto
   
    inStates = findOtherInitialStates(initialState, transitions) #busca saber se há mais de um estado inicial

    while inStates: #O processamento sempre começa pelo estado (ou estados) inicial, por isso, itera-se até não haver mais estados iniciais
        path.clear()
        currentState = inStates.pop(0) #estado atual do automâto. Começa como o estado inicial
        path.append(currentState) #adiciona o estado ao caminho atual
        
        for i in range(len(w)):
            nextState = findPossibleTransitions(currentState, w[i], transitions) #busca as transições partindo do estado atual

            if type(nextState) is list: #Se as transições forem uma lista, isto é, há mais de uma transição possível
                while True:
                    aux = path.copy() #Cria mais um caminho, já que eles serão ramificados agora
                    aux.append(nextState.pop()) #Coloca nesse caminho uma das transições retornadas pela findPossibleTransitions
                    currentState = aux[-1]
                    allPaths.append(aux)

                    if not nextState:
                        break

            elif nextState:
                currentState = nextState #Se só houver um caminho possível, ele vira o estado atual e atualiza o path atual
                path.append(currentState)
            else:
                break
                
        allPaths.append(path) #Com um caminho terminado, adiciona ele à lista que contém todos os paths


    # Checa se todos os caminhos estão em sua capacidade máxima, isto é, se houver algum caminho
    # que ainda possui transições possíveis, ele será completado.
    # Este problema surge da ramificação feita anteriormente, onde caminhos se dividiram por haver mais de uma transição
    # possível.
    
    for i in range(len(allPaths)):
        while len(allPaths[i]) <= len(w):
            index = len(allPaths[i]) - 1
            possible = findPossibleTransitions(allPaths[i][index], w[index], transitions)
            if type(possible) is list:
                while True:
                    aux = allPaths[i].copy()
                    #Old path must be removed
                    if len(possible) == 1:
                        allPaths.remove(allPaths[i])
                        
                    aux.append(possible.pop())
                    allPaths.append(aux)

                    if not possible:
                        break

            elif possible:
                allPaths[i].append(possible)
            else:
                break
    
    # Foi notado que alguns caminhos estavam no seu caminho máximo - 1, isto é, faltava apenas mais um caractere para ser processado.
    # Portanto, o processo é feito novamente para esses caminhos

    for i in range(len(allPaths)):
        if len(allPaths[i]) >= len(w):
            lastReach = findPossibleTransitions(allPaths[i][-1], w[-1], transitions)
            if type(lastReach) is list:
                while True:
                    aux = allPaths[i].copy()

                    if len(lastReach) == 1:
                        allPaths.remove(allPaths[i])

                    aux.append(lastReach.pop())
                    allPaths.append(aux)

                    if not lastReach:
                        break

            elif lastReach:
                allPaths[i].append(lastReach)
    
    if allPaths:
        return allPaths

    return None

# dropDuplicates() remove os caminhos repetidos, 'limpando' o processamento na hora de ser impresso
#
# Params:
#   allPaths: lista aninhada com todos os caminhos
#
# Return:
#   Retorna allPaths tratado, ou seja, sem itens duplicados

def dropDuplicates(allPaths):
    noDuplicates = list()
    for i in range(len(allPaths)):
        if allPaths[i] not in noDuplicates:
            noDuplicates.append(allPaths[i])
    return noDuplicates

# dropOverlengthPaths() remove caminhos que possuem caminhos excessivos, já que na teoria não era para eles existirem.
#
# Params:
#   allPaths: lista aninhada com todos os caminhos
#   w: cadeia de entrada
#
# Return:
#   Retorna os caminhos tratados

def dropOverlengthPaths(allPaths, w):
    noDuplicates = allPaths.copy()
    for path in noDuplicates:
        while len(path) > len(w) + 1:
            path.pop()
    
    return noDuplicates

# printPaths() exibe no terminal todos os processamentos calculados.
#
# Params:
#   allPaths: lista aninhada com todos os caminhos
#   w: cadeia de entrada
#   finalStates: lista com os estados finais
#
# Return:
#   Retorna um booleano que diz se a cadeia foi aceita pelo automâto ou não.
#    

def printPaths(allPaths, w, finalStates):
    arrow = u'\u2193' #unicode downwards arrow symbol
    process_counter = 1
    isAccepted = False

    allPaths = dropOverlengthPaths(allPaths, w)
    allPaths = dropDuplicates(allPaths)

    for path in allPaths:
        print('===================================================')
        print(f'\tStarting process {process_counter}')
        print('===================================================\n')

        if len(path) >= len(w):
            for i in range(len(w)):
                print(f'\t{path[i]} --------------- {w[i]}')
                print(f'\t{arrow}')
                time.sleep(0.5)

            if path[-1] not in finalStates:
                print('\t' + path[-1])
                print(f'\t{arrow}')
                print('\tX')
                print('\nThis process is not accepted by the NFA\n')
            else:
                print('\t' + path[-1])
                print('\nThis process is accepted by the NFA\n')
                isAccepted = True #Só é verdadeiro se a cadeia de entrada for totalmente lida e termina no estado final.
        
        elif len(path) < len(w):
            for i in range(len(path)):
                print(f'\t{path[i]} --------------- {w[i]}')
                print(f'\t{arrow}')
                time.sleep(0.5)

            print('\tX')
            print('\nThis process is not accepted by the NFA\n')
        
        process_counter += 1

    print(f'\nFinished processing.')

    return isAccepted

# Função principal do programa, apenas chama as outras funções e as organiza.
#
# Params:
#   filename: nome do arquivo que vai ser lido.
#
# Return:
#   Não há valor de retorno

def afn(filename):
    alphabet, states, initialState, finalStates, transitions = ir.readInputs(filename)

    w = list(input("Insira a cadeia de entrada: "))

    #Error check in the input string
    for char in w:
        if char not in alphabet:
            print("Cadeia de entrada inválida")
            sys.exit()
    
    processment_result = processment(initialState, w, transitions)

    if printPaths(processment_result, w, finalStates):
        print('\033[1;32mCadeia aceita pelo automato!\n')
    else:
        print('\033[1;31mCadeia negada pelo automato!\n')

def main():
    filename = input("Insira o nome do arquivo a ser lido (digite '.txt' ao final do nome): ")
    afn(filename)

if __name__ == '__main__':
    main()