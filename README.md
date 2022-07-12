# NFA Simulator
This is the final project of Authomata Theory, given by professor Bruno Bruck. The project is a Non-deterministic Finite Authomata Simulator, made by the students Jonas Gabriel and João Henrique.

## Installation
- `1: On this repository, click on "code" and copy the HTTPS link.`
- `2: Clone the repository to a folder usign Git bash.`
- `3: Make sure that you have Python 3 installed in your machine.`
- `4: Open a terminal and type "python3 AFN.py".`

## How to use
To use the simulator, first you will need a file .txt containing the specific format:

  `alfabeto=a,b,c\n`
  `estados=q0,q1,q2`
  `inicial=q0`
  `finais=q4`
  `transicoes`
  `q0,q1,a`
  `q1,q2,b`
  `q1,q2,epsilon`
   
Where "alfabeto" stands to authomata alphabet, "estados" to his states, "inicial" to the initial state, "finais" to the final state (can be more than one) and "transicoes" to all the authomata transitions, including epsilon transitions.

With this file ready, is necessary to put it in the same folder of the code.
