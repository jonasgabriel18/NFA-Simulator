import re

def readInputs(filename):
    alphabetPattern = '^alfabeto=\w(,\w)*'
    statePattern = '^estados=q\d(,q\d)*'
    initialStatePattern = '^inicial=q\d'
    finalStatesPattern = '^finais=(q\d)*(,q\d)*'
    transitionsPattern = '^transicoes\nq\d,q\d,\w(\nq\d,q\d,\w)' #re.match(pattern, string, re.M) to detect newlines

    with open(filename, 'r') as f:
        for lines in f:
            lines.strip()
            result = re.search(alphabetPattern, lines)
            if result:
                alphabet = result.string
                alphabet = alphabet.replace('alfabeto=', '')
                alphabet = alphabet.replace('\n', '')
                alphabet = alphabet.split(',')
                print(alphabet)

readInputs('teste.txt')