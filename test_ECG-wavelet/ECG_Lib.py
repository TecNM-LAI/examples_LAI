import serial
import sys
import glob
import struct



class ECG(object):
    def __init__(self):
        self.port = "COM0"
        self.baudrate = "115200"
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        '''self.serialCOM = serial.Serial(self.port,
                            baudrate=self.baudrate,
                            parity=self.parity,
                            stopbits=self.stopbits)'''
        self.serialCOM = []

    def available_ports(self):
        if(sys.platform.startswith('win')):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif(sys.platform.startswith("linux") or sys.platform.startswith("cygwin")):
            # Esto excluye la terminal actual "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif(sys.platform.startswith("darwin")):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Sistema operativo no soportado!")

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def open_device(self, COM, baudrate, parity, stopbits):
        self.port = COM
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.serialCOM = serial.Serial(self.port,
                            baudrate=self.baudrate,
                            parity=self.parity,
                            stopbits=self.stopbits)
        if not(self.serialCOM.isOpen()):
            self.serialCOM.open()
            print("ECG@{0} abierto".format(self.port), self.serialCOM.isOpen())
        else:
            print("ECG@{0} no se pudo abrir o ya lo estaba".format(self.port), self.serialCOM.isOpen())
            
    def close_device(self):
        self.serialCOM.close()
        if not(self.serialCOM.isOpen()):
            self.serialCOM.open()
            print("ECG@{0} cerrado".format(self.port), self.serialCOM.isOpen())
        else:
            self.serialCOM.close()
            print("ECG@{0} no se pudo cerrar".format(self.port), self.serialCOM.isOpen())

    def flush_buffer(self):
        self.serialCOM.flushInput()

    def get_payload_norm(self, printPayload, x_min, x_max):
        #self.serialCOM.write(b';')
        bytes_ECG = self.serialCOM.readline()
        data = bytes_ECG.decode("utf-8")
        x_norm = (int(data) - x_min) / (x_max - x_min)
        if(printPayload == True):
            print("ADC: {0}".format(x_norm))
            print("------------------------------------------------------------\r\n")
        return(x_norm)

    def get_payload_parsed(self, printPayload):
        #self.serialCOM.write(b';')
        bytes_ECG = self.serialCOM.readline()
        data = bytes_ECG.decode("utf-8")
        if(printPayload == True):
            print("ADC: {0}".format(data))
            print("------------------------------------------------------------\r\n")
        return(int(data))
  
    def get_payload_raw(self, printPayload):
        #self.serialCOM.write(b';')
        bytes_ECG = self.serialCOM.readline()
        if(printPayload == True):
            print(bytes_ECG)
            print("------------------------------------------------------------\r\n")
        return(payload)
