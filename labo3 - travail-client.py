import socket
import threading
import sys



class Chat:
    def __init__(self,pseudo = "Ctulhu", host=socket.gethostname(),
                 port=5000, IPServer = "0.0.0.0"):
        
        self.__pseudo = pseudo      
        self.__port = port
        self.__IPServer = IPServer
        
        s = socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s = s
        
        print('Listening on {}:{}'.format(host, port))


    def run(self):
        option = {
               '/exit' : self._exit,
               '/leave': self._leave,
               '/join': self._join,
               '/send': self._send,
               '/server': self._server
               }
            
            
        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive).start()
       
        while self.__running:
            
            line = sys.stdin.readline().rstrip() + ' '
            command = line[:line.index(' ')]
            param = line [line.index(' ')+1:].rstrip()

            if command in option:
                try:
                    option[command]() if param == '' else option[command](param)

                except:
                    print("Erreur d'exécution")
            else:
                print("Commande inconnue", command)


    def _exit(self):
        self.__running = False
        self.__adress = None
        self._server("/exit")
        self.__s.close()


    def _leave(self):
        self.__adress = None


    def _join(self, info):
        token = info.split(' ')
        if len(token) == 2:
            try:
                self.__address = (socket.gethostbyaddr(token[0])[0],
                                  int(token[1]))
                print('Connect to {}:{}'.format(*self.__address))

            except OSError:
                print("Joining error")


    def _send(self, info):
        if self.__address is not None:
            try:
                message = info.encode()
                total = 0
                
                while total < len(message):
                    sent = self.__s.sendto(message[total:],
                                           self.__address)
                    total += sent

            except OSError:
                print("Sending error")



    def _receive(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(1024)
                print(data.decode())
                sys.stdout.flush() #problème parfois si pas dans CMD

                
            except socket.timeout:
                pass
           
            except OSError:
                return
    

    def _server(self, param):
        total = 0
        try:
            s = socket.socket()
            s.connect(("172.17.34.138", 6000))
            
            message = param + ' ' + str(self.__port) + ' ' + self.__pseudo
            message = message.encode()
            
            while total < len(message):
                sent = s.send(message[total:])
                total += sent
    
            s.close()
            
        except OSError:
            print('Couldn\'t connect to the server')
                        




if __name__ == '__main__':
    if len(sys.argv) == 4:
        Chat(sys.argv[1], int(sys.argv[2]), sys.argv[3]).run()
    else:
        Chat().run()


