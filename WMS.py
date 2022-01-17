import os
import sys
import json
import asyncio
import websockets

from dotenv          import load_dotenv
from os.path         import join, dirname
from PyQt5           import uic
from PyQt5.QtWidgets import QMainWindow,QApplication
from IPy             import IP


global IP_ADDRESS
global PORT

IP_ADDRESS   = "127.0.0.1"
PORT = 8766

class WEBSOCKET_WINDOW(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("UI/websocket.ui",self)

        IP_ADDRESS_SPLITED = IP_ADDRESS.split(".")

        self.le_IP_1.setText(str(IP_ADDRESS_SPLITED[0]))
        self.le_IP_2.setText(str(IP_ADDRESS_SPLITED[1]))
        self.le_IP_3.setText(str(IP_ADDRESS_SPLITED[2]))
        self.le_IP_4.setText(str(IP_ADDRESS_SPLITED[3]))

        self.le_PORT.setText(str(PORT))

        self.pb_act_websocket.clicked.connect(self.act_websocket)

    def act_websocket(self):
        res = self.validate_IPv4()
        if res:
            # IP VALIDA
            self.l_message_IP.setStyleSheet("color: green")
            self.l_message_IP.setText("IP valida")

            if self.validate_PORT():
                #IP y PUERTO VALIDOS
                self.l_message_PORT.setStyleSheet("color: green")
                self.l_message_PORT.setText("Puerto valido")

                self.close()
            else:
                self.l_message_PORT.setStyleSheet("color: red")
                self.l_message_PORT.setText("Puerto NO valido")
            
        else:
            # IP NO VALIDA
            self.l_message_IP.setStyleSheet("color: red")
            self.l_message_IP.setText("IP invalida")
            
            if self.validate_PORT():
                #IP y PUERTO VALIDOS
                self.l_message_PORT.setStyleSheet("color: green")
                self.l_message_PORT.setText("Puerto valido")
            else:
                self.l_message_PORT.setStyleSheet("color: red")
                self.l_message_PORT.setText("Puerto NO valido")
            
    def validate_IPv4(self):    
        IP_1 = str(self.le_IP_1.text())
        IP_2 = str(self.le_IP_2.text())
        IP_3 = str(self.le_IP_3.text())
        IP_4 = str(self.le_IP_4.text())

        IP_ADDRESS_TO_VALIDATE = IP_1 + "." + IP_2 + "." + IP_3 + "." + IP_4

        try:
            IP(IP_ADDRESS_TO_VALIDATE)
            global IP_ADDRESS
            IP_ADDRESS = IP_ADDRESS_TO_VALIDATE
            return True
        except:
            return False

    def validate_PORT(self):
        #Puertos bien conocidos y restringidos: 0 - 1023 (Para protocolos como HTTP, SMTP, FTP, DNS,... etc)
        #Puertos registrados: 1024 - 49151 (Para aplicaciones tipo SERVIDOR Son 48127 puertos)
        #Puertos dinámicos/efímeros: 49151 - 65535 (Para aplicaciones tipo CLIENTE. Son 16354 puertos)
        
        try:
            PORT_TO_VALIDATE = int(self.le_PORT.text())
            if PORT_TO_VALIDATE >= 0 and PORT_TO_VALIDATE <= 65535:
                global PORT
                PORT = PORT_TO_VALIDATE
                return True
            else:
                return False
        except:
            return False
        



class WMS(QMainWindow):

    
    SKU      = ""
    QUANTITY = ""
    SHELF    = ""

    PATHFILE = ""
    
    request = {"sku":"",
               "quantity":"",
               "shelf":""}

    window = None

    json_request = None

    def __init__(self):
        super().__init__()

        dotenv_path = join(dirname(__file__), 'EnvFile.env')
        load_dotenv(dotenv_path)

        #loads WMS main window
        uic.loadUi("UI/WMS.ui",self)

        #connect events with qwidgets
        self.pb_send_request.clicked.connect(self.fn_send_Request)
        self.pb_websocket.clicked.connect(self.show_websocket_window)


    def fn_send_Request(self):
        try:
            #Retrieve data from GUI
            self.SKU      = str(self.le_sku.text())
            self.QUANTITY = str(self.le_quantity.text())
            self.SHELF    = str(self.le_shelf.text())

            #Build message
            self.request  = {"sku":self.SKU,
                             "quantity":self.QUANTITY,
                             "shelf":self.SHELF}
            self.json_request = json.dumps(self.request, indent=4, sort_keys=False)

            #Send message
            self.send_request()

        except:
            pass
        

    def send_request(self):
        asyncio.get_event_loop().run_until_complete(self.send_message())

    async def send_message(self):
        global IP_ADDRESS
        global PORT
        uri = "ws://" + str(IP_ADDRESS) + ":" + str(PORT)
        async with websockets.connect(uri) as websocket:
            await websocket.send(self.json_request)

    
    def show_websocket_window(self):
        #self.window = QMainWindow()
        self.window = WEBSOCKET_WINDOW()
        #self.hide()
        self.window.show()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    GUI = WMS()
    #GUI = WEBSOCKET_WINDOW()
    GUI.show()
    sys.exit(app.exec_())
    
    print("termine")
    input()