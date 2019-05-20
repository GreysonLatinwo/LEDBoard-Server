#gets client connects to us, and the server gets the data sent from client
#then we return the data that we got.
import socket, select, os, sys
class socketServer:

    def startServer(self):
        data = None
        HOST = ''
        PORT = 6969

        CONNECTION_LIST = []
        RECV_BUFFER = 2048

        serverSocket = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        CONNECTION_LIST.append(serverSocket)

        try:
                serverSocket.bind((HOST, PORT))
        except socket.error as err:
                print("couldnt bind with the ip")
                serverSocket.close()
                sys.exit()
        serverSocket.listen()

        print("Listening...")
        while data is None:
            read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
            for sock in read_sockets:
                if sock == serverSocket:
                    sockfd, addr = serverSocket.accept()
                    CONNECTION_LIST.append(sockfd)
                    print("Client (%s, %s) connected" % addr)

                else:
                    try:
                        data = sock.recv(RECV_BUFFER).decode('ascii')
                        #print(data)
                    finally:
                        print("Client Disconnected")
                        CONNECTION_LIST.remove(sock)
                        sock.close()
                        #serverSocket.close()
#                   serverSocket.shutdown(socket.SHUT_RDWR)
        return data