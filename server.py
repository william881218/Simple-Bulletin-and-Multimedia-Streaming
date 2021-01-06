import socket
import threading
import sqlite3 as sql

from html_parser import HTMLParser
from http_parser import HTTPParser


class Server():
    '''
    Basic socket that supports multithreading.
    '''
    def __init__(self, port, host='127.0.0.1', buf_size=4096):

        self.host = host
        self.port = port
        self.buf_size = buf_size
        self.alive_connection = 0

        # initialize html parser, http parser and database
        self.html_parser = HTMLParser(template='templates/index.html')
        self.http_parser = HTTPParser()

        # initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # configure socket

        # bind socket onto certain port
        self.socket.bind((self.host, self.port))
    

    def run(self):
        '''
        Start listening on specific port.
        '''
        self.socket.listen(30)

        # everytime we've accept a client, initialize a new thread to handle connection
        while True:
            client_socket, addr = self.socket.accept()
            self.alive_connection += 1
            client_socket.settimeout(10) # any connection being idle for > 180 sec will be closed
            print("New connection: {}".format(self.alive_connection), flush=True)
            threading.Thread(target=Server.client_connection,
                             args=(self, client_socket, addr)).start()
        

    def client_connection(self, client_socket, addr):
        
        while True:
            try:
                received_response = client_socket.recv(self.buf_size)

                if received_response:

                    # Set the response to echo back the recieved data 
                    received_response = received_response.decode()
                    #print('====== received data =====')
                    #print(received_response)
                    #print('======')

                    # determine the http type of received_response
                    http_method, url = HTTPParser.get_method(received_response)
                    #print('method: {}, url: {}'.format(http_method, url))

                    # handle received response
                    self.html_parser.update_documents(received_response)

                    # generate response to the client server
                    html_response = self.html_parser.generate_response()
                    #print('====== html response =====')
                    #print(html_response)

                    # wrap the html response into http response
                    http_response = self.http_parser.parse(text=html_response)
                    #print('==== http response=====')
                    #print(http_response)

                    #print('=======end=======', flush=True)

                    client_socket.send(http_response.encode())
                
                # the client has closed the connection or timed out
                else:
                    raise socket.timeout

            except:
                client_socket.close()
                self.alive_connection -= 1
                print('===thread closed! alive: {}======'.format(self.alive_connection), flush=True)
                break

