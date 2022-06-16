import re #importa regex

# errorCheck() vai checar se todos os elementos passados no arquivo estão corretos.
#
# @Params:
#   alphabet: caracteres do alfabeto aceito pelo AFN
#   states: estados do AFN
#   initialState: estado inicial do AFN
#   finalStates: estado final do AFN (pode ser mais de um)
#   transitions: todas as transições do AFN
#
# Retorna True caso haja algum erro nos inputs
# Retorna False caso esteja tudo certo

def errorCheck(alphabet, states, initialState, finalStates, transitions):

    if not alphabet:
        print('Não foi possível ler o alfabeto\n')
        return True
    elif not states:
        print('Não foi possível ler os estados\n')
        return True
    elif not initialState:
        print('Não foi possível ler o estado inicial\n')
        return True
    elif not transitions:
        print('Não foi possível ler as transições\n')
        return True

    if initialState not in states:
        print(f'O estado inicial {initialState} não está contido nos estados\n')
        return True
    
    if not finalStates and finalStates not in states:
        print(f'Os estados finais {finalStates} não estão contidos nos estados\n')
        return True

    for transition in transitions:
        for i in range(len(transition)):
            if i == 2:
                if transition[i] not in alphabet and transition[i] != 'epsilon':
                    print(f'A transição {transition} é inválida, pois o elemento de transição não está contido no alfabeto\n')
                    return True
            else:
                if transition[i] not in states:
                    print(f'A transição {transition} é inválida, pois algum dos estados de transição não está contido nos estados\n')
                    return True
    
    return False

# readInputs() é a função responsável por ler o arquivo.
# 
# @Params:
#   filename: nome do arquivo a ser lido
#
# Retorna todos os inputs do AFN, sendo eles: alfabeto, estados, estado inicial, estado final (pode ser mais de um)
# e uma lista aninhada contendo as transições
#
# Exceções:
#   FileNotFoundError: se o arquivo passado como parâmetro estiver com o nome correto ou não está no mesmo diretório
#   IOError: se por algum motivo não foi possível fazer a leitura do arquivo

def readInputs(filename):

    if not filename.endswith('.txt'): #apenas checa arquivos .txt
        print(f'O arquivo {filename} não possui o formato .txt\n')
        return None

    # Foi utilizado Expressões Regulares para capturar os padrões de como os inputs devem vir no arquivo
    # O alphabetPattern aceita alfabetos com letras (Ex: a,b,c) e com números (Ex: 0,1,2)
    # O statePattern detecta quaisquer letras 'q' seguidas de um dígito no intervalo [0, 9]
    # initialPattern retorna apenas uma letra 'q' seguida de um dígito
    # finalStatePattern busca um ou mais estado no formato de 'q' seguido por um dígito
    # transitionsPattern busca pelo formato de dois estados separados por vírgula e seguido por letras ou números
    # Foi utilizado o site regex101.com para testar os padrões

    alphabetPattern = '^alfabeto=(\w(,\w)*)|(\d(,\d)*)'
    statePattern = '^estados=q\d(,q\d)*'
    initialStatePattern = '^inicial=q\d'
    finalStatesPattern = '^finais=(q\d)*(,q\d)*'
    transitionsPattern = '^q\d,q\d,\w'

    alphabet = list()
    states = list()
    finalStates = list()
    transitions = list()

    try:
        with open(filename, 'r') as f: # Abertura do arquivo para leitura
            for lines in f:
                lines.strip()

                alphabet_result = re.search(alphabetPattern, lines) #Função searcho do regex busca pelo padrão em uma string (lines nesse caso)
                states_result = re.search(statePattern, lines)
                initialState_result = re.search(initialStatePattern, lines)
                finalStates_result = re.search(finalStatesPattern, lines)

                if alphabet_result and not alphabet:
                    alphabet = alphabet_result.string.replace('alfabeto=', '').replace('\n', '').split(',') # Remove o que não queremos do padrão
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
        print(f'O arquivo {filename} não foi encontrado\n')
        return None
    except IOError:
        print(f'Não foi possível abrir/ler o arquivo {filename}\n')
        return None
    except:
        print('Erro inesperado\n')
        return None
                
    if errorCheck(alphabet, states, initialState, finalStates, transitions):
        print('Erro na leitura do arquivo\n')
        return None

    print('Sucesso na leitura do arquivo\n')

    return alphabet, states, initialState, finalStates, transitions