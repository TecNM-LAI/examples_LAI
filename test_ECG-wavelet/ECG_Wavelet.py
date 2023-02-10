from ECG_Lib import ECG

import time
import serial
import sys

import numpy as np
import math
import matplotlib.pyplot as plt
import pywt



def main():
    # Declaracion de variables
    Sf = 1000     
    S = 16000

    a = float(0.7284895)
    b = float(0.13575525)
    xn1 = float(0.0)
    yn1 = float(0.0)
    
    try:
        dedal = ECG()
        print(dedal.available_ports())
        dedal.open_device(COM = "COM14", baudrate = "115200",
                          parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)
        dedal.flush_buffer()
        
        # Inicializacion de la grafica de la señal original
        fig, axis = plt.subplots(3,1,figsize=(15,7))
        fig.show()

        while(True):
            ecg_signal = []
            xn = []
            time.sleep(1)
            dedal.flush_buffer()
            
            #Obtencion de datos via serial
            print("Capturando la señal del ECG...")
            print()
            for j in range(S):
                # Obtener y normalizar la señal
                '''xn.append(dedal.get_payload_norm(printPayload = False,
                                                 x_min = 500, x_max = 525))'''
                # Obtener la señal original
                xn.append(dedal.get_payload_parsed(printPayload = False))

            print("Filtrando la señal...")
            print()
            # Filtrado de la señal (LPF, cf = 0.5 Hz)
            for j in range(S):
                # Computar la señal filtrada
                yn = a*yn1 + b*xn[j] + b*xn1
                xn1 = xn[j]
                yn1 = yn
                ecg_signal.append(yn)
                
            '''if(len(x) >= 300):
                x = x[-300:]

                # Computar la DWT
                cA, cD = pywt.dwt(x, 'sym4', 'smooth')
                # Computar la reconstruccion
                #y = pywt.idwt(cA, cD, 'bior6.8', 'per')'''

            '''print("Graficando la señal original y la filtrada...")
            print()
            for j in range(S):
                axis[0].clear()
                axis[0].plot(xn, color = 'g')
                axis[0].set_title("Señal original")
                axis[0].set_ylabel("y[n]")
                axis[0].set_xlabel("n")
                fig.canvas.draw()
                axis[0].set_ylim([500, 525])
                axis[0].set_xlim(left = max(0, j - S), right = (j + 5))
                plt.pause(0.001)
                
                axis[1].clear()
                axis[1].plot(ecg_signal, color = 'b')
                axis[1].set_title("Señal filtrada")
                axis[1].set_ylabel("y[n]")
                axis[1].set_xlabel("n")
                fig.canvas.draw()
                axis[1].set_ylim([500, 525])
                axis[1].set_xlim(left = max(0, j - S), right = (j + 5))
                plt.pause(0.001)'''

            print("Graficando la señal original y la filtrada...")
            print()
            axis[0].clear()
            axis[0].plot(xn, color = 'g')
            axis[0].set_title("Señal original")
            axis[0].set_ylabel("y[n]")
            axis[0].set_xlabel("n")
            fig.canvas.draw()
            axis[0].set_ylim([500, 525])
            axis[0].set_xlim(left = max(0, S - S), right = (S + 5))
            plt.pause(0.001)
                
            axis[1].clear()
            axis[1].plot(ecg_signal, color = 'b')
            axis[1].set_title("Señal filtrada")
            axis[1].set_ylabel("y[n]")
            axis[1].set_xlabel("n")
            fig.canvas.draw()
            axis[1].set_ylim([500, 525])
            axis[1].set_xlim(left = max(0, S - S), right = (S + 5))
            plt.pause(0.001)
                
            print("Pasando a la DWT...")
            print()
            time.sleep(1.5)

            print("Cálculo de la DWT...")
            print()
            cA, cD = pywt.dwt(ecg_signal, 'sym4', 'periodic')
            coeffs = pywt.wavedec(xn, 'sym4', level=8, mode='periodic')
            cA8, cD8, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs

            '''print("Graficando la señal procesada...")
            print()
            for j in range(len(cD4)):
                axis[2].clear()
                axis[2].plot(cD4, color = 'r')
                axis[2].set_title("DWT")
                axis[2].set_ylabel("y[n]")
                axis[2].set_xlabel("n")
                fig.canvas.draw()
                axis[2].set_ylim([-20, 20])
                axis[2].set_xlim(left = max(0, j - len(cD4)), right = (j + 1))
                plt.pause(0.001)'''

            print("Graficando la señal procesada...")
            print()
            axis[2].clear()
            axis[2].plot(cD6, color = 'r')
            axis[2].set_title("DWT")
            axis[2].set_ylabel("y[n]")
            axis[2].set_xlabel("n")
            fig.canvas.draw()
            axis[2].set_ylim([-10, 10])
            axis[2].set_xlim(left = max(0, len(cD6) - len(cD6)), right = (len(cD6) + 1))
            plt.pause(0.001)

            #time.sleep(3)
  
    except(KeyboardInterrupt):
        dedal.flush_buffer()
        dedal.close_device()
        plt.close('all')
        sys.exit()



if __name__ == '__main__':
    main()
