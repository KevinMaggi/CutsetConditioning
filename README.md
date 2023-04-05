# Overview
Questo progetto è parte dell'esame di *Intelligenza artificiale* tenuto dal Prof. *Paolo Frasconi* nella Laurea Triennale in Ingegneria Informatica all'Università degli Studi di Firenze.
- Anno accademico: 2019/2020
- Titolo del progetto: Cutset Conditioning
- Studente: Kevin Maggi
- CFU: 6

> :warning: **Attenzione**: come si può vedere questo progetto è disponibile pubblicamente e chiunque è ovviamente libero di trarre spunto da esso. Tuttavia se verrà trovato che qualcuno sta copiando il codice (nel senso CTRL-C / CTRL-V) per il suo progetto dello *stesso* esame, sarà segnalato al Professore.

# Cutset Conditioning

- I file Variable.py, Constraint.py, CSP.py e Assignment.py contengono le classi che rappresentano rispettivamente le variabili, i vincoli, i CSP e gli assegnamenti.

- I file AC3.py, Backtrack.py, TreeSolver.py e Cutset.py contengono gli algoritmi AC3, Backtracking, TreeSolver e Cutset e le funzioni ausiliari.

- Il file Map.py contiene le classi relative alle mappe e l'algoritmi per la loro generazione casuale.

- Il file main.py contiene la funzione di test: per replicare i test è sufficiente eseguire questo; si può agire su alcuni parametri (come il numero massimo di variabili, lo step di aumento del numero di variabili e il numero di test da effettuare) che si trovano come variabili globali all'inizio del file.

- Il file Example.py contiene alcuni esempi di semplici csp e alcune funzioni che mostrano il funzionamento degli algoritmi.
