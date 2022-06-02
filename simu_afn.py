import Input_Reader as I_R
import threading
import time

alfabeto, estados, ei, ef, transicoes=I_R.readInputs(teste)

def worker(#um estado
):
    for i in range(#quantidade de transicoes desse estado
    ):
        #criar threads nessa quantidade de transicoes, sendo uma thread para cada possibilidade 