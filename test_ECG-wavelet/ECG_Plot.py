from ECG_Lib import ECG

import time
import serial
import sys

import numpy as np
import math
import matplotlib.pyplot as plt



    
def main():
    dedal = ECG()
    print(dedal.available_ports())
    dedal.open_device(COM = "COM14", baudrate = "9600",
                     parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)
    dedal.flush_buffer()
    # Inicializacion de la grafica de la señal original
    fig1 = plt.figure(figsize = (7,4))
    ax1 = fig1.add_subplot()
    fig1.show()
    try:
        x = []
        i = 0
        xn1 = float(0.0)
        yn1 = float(0.0)
        S = 300
        dedal.flush_buffer()
        while(True):
            '''arreglo = []
            for i in range(1000):
                data = dedal.get_payload_parsed(printPayload = False)
                #print(data)
                #print()
                arreglo.append(data)
                sleep(0.001)
            print("Min: ")
            print(min(arreglo))
            print("Max: ")
            print(max(arreglo))
            print("--------")'''

            # Normalizar la señal
            '''xn = dedal.get_payload_norm(printPayload = False,
                                          x_min = 500, x_max = 525)'''

            # Obtener la señal
            xn = dedal.get_payload_parsed(printPayload = False)

            x.append(xn)
            if(len(x) >= S):
                x = x[-S:]
                
            ax1.clear()
            ax1.plot(x, color = 'g')
            ax1.set_title("Señal original")
            ax1.set_ylabel("y[n]")
            ax1.set_xlabel("n")
            fig1.canvas.draw()
            
            ax1.set_ylim([500, 525])
            ax1.set_xlim(left = max(0, i - S), right = (i + 5))
            
            if(i < S):
                i = i + 1
            plt.pause(0.0001)
            #sleep(0.001)
  
    except(KeyboardInterrupt):
        dedal.flush_buffer()
        dedal.close_device()
        plt.close('all')
        sys.exit()



if __name__ == '__main__':
    main()
