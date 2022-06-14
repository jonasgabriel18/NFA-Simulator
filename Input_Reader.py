import re
import time

def errorCheck(alphabet, states, initialState, finalStates, transitions):

    if not alphabet or not states or not initialState or not transitions:
        print('Alguma entrada está vazia')
        return True
    
    if initialState not in states:
        print(f'O estado inicial {initialState} não está contido nos estados')
        return True
    
    if not finalStates and finalStates not in states:
        print(f'Os estados finais {finalStates} não estão contidos nos estados')
        return True

    for transition in transitions:
        for i in range(len(transition)):
            if i == 2:
                if transition[i] not in alphabet and transition[i] != 'epsilon':
                    print(f'A transição {transition} é inválida, pois o elemento de transição não está contido no alfabeto')
                    return True
            else:
                if transition[i] not in states:
                    print(f'A transição {transition} é inválida, pois algum dos estados de transição não está contido nos estados')
                    return True
    
    return False

def readInputs(filename):

    if not filename.endswith('.txt'):
        print(f'O arquivo {filename} não possui o formato .txt')
        return None

    alphabetPattern = '^alfabeto=(\w(,\w)*)|(\d(,\d)*)'
    statePattern = '^estados=q\d(,q\d)*'
    initialStatePattern = '^inicial=q\d'
    finalStatesPattern = '^finais=(q\d)*(,q\d)*'
    transitionsPattern = '^q\d,q\d,\w'

    alphabet = []
    states = []
    finalStates = []
    transitions = []

    try:
        with open(filename, 'r') as f: #falta checar se há erro no arquivo passado (se existe, se não for txt etc)
            for lines in f:
                lines.strip()

                alphabet_result = re.search(alphabetPattern, lines)
                states_result = re.search(statePattern, lines)
                initialState_result = re.search(initialStatePattern, lines)
                finalStates_result = re.search(finalStatesPattern, lines)

                if alphabet_result and not alphabet:
                    alphabet = alphabet_result.string.replace('alfabeto=', '').replace('\n', '').split(',')
                elif states_result and not states:
                    states = states_result.string.replace('estados=', '').replace('\n', '').split(',')
                elif initialState_result:
                    initialState = initialState_result.string.replace('inicial=', '').replace('\n', '')
                elif finalStates_result and not finalStates:
                    finalStates = finalStates_result.string.replace('finais=', '').replace('\n', '').split(',')
                elif lines == 'transicoes\n':
                    for line in f:
                        transitions_result = re.search(transitionsPattern, line)
                        if transitions_result:
                            transitions.append(transitions_result.string.replace('\n', '').split(','))
    except FileNotFoundError:
        print(f'O arquivo {filename} não foi encontrado')
        return None
    except IOError:
        print(f'Não foi possível abrir/ler o arquivo {filename}')
        return None
    except:
        print('Erro inesperado')
        return None
                
    
    if errorCheck(alphabet, states, initialState, finalStates, transitions):
        print('Erro na leitura do arquivo')
        return None


    print('Sucesso na leitura do arquivo')
    return alphabet, states, initialState, finalStates, transitions
