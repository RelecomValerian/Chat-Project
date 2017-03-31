import socket
import sys



class Server:
    def __init__(self, host=socket.gethostname(), port=6000):    
        self.__s = socket.socket()
        self.__s.bind((host, port))
        self.__clients = {}    # dico des clients
        print('Ecoute à {} : {}'.format(host,port))


    def run(self):
        self.__s.listen()
        option = {"/clients" : self._clients,
                  "/exit" : self._exit
                  }

        while True:
            try:
                client, addr = self.__s.accept()
                
                line = self._receive(client).decode() + ' '
                line = line.split(' ')
                command = line[0]
                port = line[1]
                pseudo = line[2]
                
                if pseudo not in self.__clients:
                    self.__clients[pseudo] = [addr[0], port]
                    
                if command in option:
                    try:
                        option[command](addr, port, pseudo)
                        
                    except:
                        print("Erreur d'exécution")


            except TypeError:
                print("Something went Wong")


    def _clients(self, addr, port, pseudo):
        s = socket.socket(type=socket.SOCK_DGRAM)
        address = (socket.gethostbyaddr(addr[0])[0]
                   , int(port))

        for el in self.__clients:
            message = "{} : {}, {}".format(el, *self.__clients[el])
            message = message.encode()
            dataSent = 0
            while dataSent < len(message):
                sent = s.sendto(message[dataSent:], address)
                dataSent += sent
                
        s.close()


    def _exit(self, addr, port, pseudo):
        del self.__clients[pseudo]
        print(self.__clients)
        

    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)



if __name__ == '__main__':
    if len(sys.argv) == 3:
        Server(sys.argv[1], int(sys.argv[2])).run()

    else:
        Server().run()
        
