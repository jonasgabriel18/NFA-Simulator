import re

pattern = '^alfabeto=\D(,\D)*'
string = 'alfabto=a,b,'
result = re.search(pattern, string)

if result:
    print(result)
else:
    print("deu ruim")

#arquivo = open('teste.txt', 'r')

#for linhas in arquivo:
 #   linhas = linhas.strip()
  #  print(linhas)

#arquivo.close()