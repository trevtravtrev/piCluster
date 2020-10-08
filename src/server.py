import socket
import threading
import json
import time

import messages


class Server:
    def __init__(self, host_ip, host_port):
        self.host = host_ip
        self.port = host_port
        self.connected = False
        self.clients = []

        self.start_server()
        self.connection_handler()
                

    def start_server(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((self.host, self.port))
                self.connected = True
                print("Server started successfully")
                break
                
            except Exception as e:
                self.connected = False
                print(f'start_server error: {e}')
                
                
    def connection_handler(self):
        while True:
            try:
                if self.connected:
                    self.sock.listen(7)
                    print("Listening for connections...")
                    
                    connection, address = self.sock.accept()
                    
                    client = ClientThread(self, connection, address)
                    client.start()
                    print(f'Client: {address} connected.')
                    
                    self.clients.append(connection)
                    print(f'{len(self.clients)} client(s) connected')
                    
                else:
                    print("Server not running. Restarting...")
                    self.start_server()

            except Exception as e:
                print(f'connection_handler error: {e}')
            
            
    def send_all(self, message):
        try:
            for client in self.clients:
                client.sendall(message)
            print(f'Message successfully sent to {len(clients)} client(s)')
            
        except Exception as e:
            print(f'send_all error: {e}')


class ClientThread(threading.Thread):
    def __init__(self, serv, connection, address):
        threading.Thread.__init__(self)
        self.server = serv
        self.conn = connection
        self.addr = address
        self.pi_num = ""


    def run(self):
        self.client_handler()
            
            
    def client_handler(self):
        while True:
            try:
                data = self.conn.recv(4096)

                if data:
                    message = messages.deserialize_data(data)
                    print(f'Message received: {message}')
                    self.message_handler(message)
                    
                else:
                    self.remove_client()
                    break
                    
            except Exception as e:
                print(f'client_handler error: {e}')
                    
        
    def message_handler(self, message):
        try:
            if "pi_num" in message.keys():
                self.pi_num = message.get('pi_num')
                print(f'pi_num: {self.pi_num}')
                
                #pull website from database
                website = "www.test123.com"
                message = messages.create_message("test", website)
                self.conn.sendall(message)
                
            elif "crawler" in message.keys():
                # add to the database
                # self.conn.sendall(another website)
                pass
                
            else:
                print("Error: function not found in keys.")
                
        except Exception as e:
            print(f'message_handler error: {e}')
            
    def remove_client(self):
        try:
            print('Client disconnected. Removing from client list...')
            self.server.clients.remove(self.conn)
            print(f'{len(self.server.clients)} clients(s) connected')
        
        except Exception as e:
            print(f'remove_client error: {e}')
        


def main():
    s = Server("192.168.86.100", 8000)


if __name__ == '__main__':
    main()
    