import re

def readInputs(filename):
    alphabetPattern = '^alfabeto=\w(,\w)*'
    statePattern = '^estados=q\d(,q\d)*'
    initialStatePattern = '^inicial=q\d'
    finalStatesPattern = '^finais=(q\d)*(,q\d)*'
    transitionsPattern = '^q\d,q\d,\w' #re.match(pattern, string, re.M) to detect newlines

    alphabet = []
    states = []
    finalStates = []
    transitions = []

    with open(filename, 'r') as f:
        for lines in f:
            lines.strip()

            alphabet_result = re.search(alphabetPattern, lines)
            states_result = re.search(statePattern, lines)
            initialState_result = re.search(initialStatePattern, lines)
            finalStates_result = re.search(finalStatesPattern, lines)

            if alphabet_result and not alphabet:
                alphabet = alphabet_result.string.replace('alfabeto=', '').replace('\n', '').split(',')
                print(alphabet)
            elif states_result and not states:
                states = states_result.string.replace('estados=', '').replace('\n', '').split(',')
                print(states)
            elif initialState_result:
                initialState = initialState_result.string.replace('inicial=', '').replace('\n', '')
                print(initialState)
            elif finalStates_result and not finalStates:
                finalStates = finalStates_result.string.replace('finais=', '').replace('\n', '').split(',')
                print(finalStates)
            elif lines == 'transicoes\n':
                for line in f:
                    transitions_result = re.search(transitionsPattern, line)
                    if transitions_result:
                        transitions.append(transitions_result.string.replace('\n', '').split(','))
                
                print(transitions)
    

    return alphabet, states, initialState, finalStates, transitions

readInputs('teste.txt')