import os
import socket
import threading

from datetime import datetime

from .html_parser import HTMLParser
from .http_parser import HTTPParser


class Server():
    '''
    Basic socket that supports multithreading.
    '''
    def __init__(self, port, host='0.0.0.0', buf_size=4096, document_dir='documents'):

        self.host = host
        self.port = port
        self.buf_size = buf_size
        self.document_dir = document_dir
        self.alive_connection = 0

        # initialize document dir related parameters
        self.document_list = [ os.path.join(self.document_dir, filename) for
                               filename in os.listdir(self.document_dir) ]
        self.document_idx = len(self.document_list)

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
            client_socket.settimeout(180) # any connection being idle for > 180 sec will be closed
            print("New connection: {}".format(self.alive_connection), flush=True)
            threading.Thread(target=Server.client_connection,
                             args=(self, client_socket, addr)).start()
        

    def client_connection(self, client_socket, addr):
        
        while True:
            received_response = client_socket.recv(self.buf_size)

            if received_response:

                # Set the response to echo back the recieved data 
                received_response = received_response.decode()

                # determine the http type of received_response
                http_method, url = HTTPParser.get_method(received_response)

                # handle received response
                if http_method == 'POST' and url == '/':
                    
                    content_len = HTTPParser.get_content_len(received_response)
                    context = HTTPParser.get_context(received_response)

                    if len(context) < content_len: # potentially will have bug if text too long
                        context = client_socket.recv(self.buf_size).decode()

                    # get name and context from client
                    context_list = context.split('\r\n\r\n')
                    client_name = context_list[1].split('------WebKitFormBoundary')[0].strip().replace('\r', '')
                    client_context = context_list[2].split('------WebKitFormBoundary')[0].strip().replace('\r','')

                    self.write_document(name=client_name, context=client_context)

                elif http_method == 'GET' and url == '/':
                    pass
                else: # non supported request type
                    print('Error: Non-supported request type: {} \"{}\". Thread closed.'.format(http_method, url), flush=True)
                    exit()

                # generate response to the client server
                html_response = self.html_parser.generate_response(self.document_list)

                # wrap the html response into http response and send
                http_response = self.http_parser.parse(text=html_response)
                client_socket.sendall(http_response.encode())
            
            # the client has closed the connection or timed out
            else:
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                self.alive_connection -= 1
                print('===thread closed! alive: {}======'.format(self.alive_connection), flush=True)
                break
                
                
    def write_document(self, name, context):
        '''
        Save document in the `self.document_dir` directory with corresponding `name` and `context`.
        '''
        filename = str(self.document_idx) + '.doc.log'
        file_path = os.path.join(self.document_dir, filename)
        cur_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # writing file
        with open(file_path, 'w') as out_file:
            out_file.write('<b>' + name + '  at ' + cur_time + '</b><br>')
            out_file.write(context.replace('\n', '<br>') + '<br>')

        self.document_idx += 1
        self.document_list.append(file_path)