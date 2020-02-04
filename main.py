from Cutset import cutset
from Backtrack import backtrack
from Map import *

import numpy as np
from timeit import default_timer as timer

import winsound
frequency = 2500
duration = 1000

NUMBER_OF_TESTS = 5
NUMBER_OF_VARIABLES = 500
STEP = 25


def test(*, minimalCutsetSize=1):
    y_bt = np.zeros(int(NUMBER_OF_VARIABLES / STEP)+1)
    y_cs = np.zeros(int(NUMBER_OF_VARIABLES / STEP)+1)
    y_sizeCs = np.zeros(int(NUMBER_OF_VARIABLES / STEP)+1)
    y_cs_h = np.zeros(int(NUMBER_OF_VARIABLES / STEP)+1)
    y_sizeCs_h = np.zeros(int(NUMBER_OF_VARIABLES / STEP)+1)
    x = np.arange(0, NUMBER_OF_VARIABLES+1, STEP)

    for i in range(NUMBER_OF_TESTS):
        for dimension in range(STEP, NUMBER_OF_VARIABLES+1, STEP):
            print('testing: ' + str(dimension) + ' #' + str(i+1), end=' ')

            map = generateMap(dimension, minimalCutsetSize=minimalCutsetSize)
            csp = map.toCSP()

            print('start')

            start = timer()
            solBt = backtrack(csp)
            end = timer()
            timeBt = end-start

            start = timer()
            solCs, size = cutset(csp, heuristic=False)
            end = timer()
            timeCs = end-start

            start = timer()
            solCs_h, size_h = cutset(csp)
            print(size_h)
            end = timer()
            timeCs_h = end-start

            y_sizeCs[int(dimension/STEP)] += dimension-size
            y_sizeCs_h[int(dimension/STEP)] += dimension-size_h
            y_bt[int(dimension/STEP)] += timeBt
            y_cs[int(dimension/STEP)] += timeCs
            y_cs_h[int(dimension/STEP)] += timeCs_h

    winsound.Beep(frequency, duration)

    y_sizeCs /= NUMBER_OF_TESTS
    y_sizeCs_h /= NUMBER_OF_TESTS
    y_bt /= NUMBER_OF_TESTS
    y_cs /= NUMBER_OF_TESTS
    y_cs_h /= NUMBER_OF_TESTS

    # PLOT SOLVING TIME
    plt.plot(x, y_bt)
    plt.plot(x, y_cs)
    plt.plot(x, y_cs_h)
    plt.legend(['Backtrack', 'Cutset senza euristica', 'Cutset con euristica'])
    plt.title('Tempo di risoluzione: backtrack vs cutset')
    plt.xlabel('Numero di variabili')
    plt.ylabel('Tempo (secondi)')
    plt.show()

    # PLOT CUTSET SIZE
    plt.plot(x, y_sizeCs)
    plt.plot(x, y_sizeCs_h)
    plt.legend(['Cutset senza euristica', 'Cutset con euristica'])
    plt.title('Dimensione cutset effettivo')
    plt.xlabel('Numero di variabili')
    plt.ylabel('Tempo (secondi)')
    plt.show()


if __name__ == "__main__":
    test(minimalCutsetSize=1)
    test(minimalCutsetSize=2)
