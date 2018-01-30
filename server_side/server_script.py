import server_imports
from server_imports import *
import retrieve #.py file containing class
from retrieve import Retrieve
import store #.py file containing class
from store import Store
import store_more
from store_more import StoreMore
import argparse



def listen_for_connection(port):
    # wait for and return open conenction
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), port))
    serversocket.listen(5)
    server_connection, address = serversocket.accept()
    return server_connection

def process_first_transmission(server_connection):
    """ Return value is 0 if client intends to upload, 1 if request. 2 if
        client wants to upload additional files"""
    value = int(server_connection.recv(30).decode(), 2)
    if value == 1048575:
        print ("File not on server. Closing connection.")
        server_connection.close()
        sys.exit()
    return value

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port', default=9998)
    args = parser.parse_args()
    return int(args.port)

if __name__ == '__main__':
    port = parse_arguments()
    connection = listen_for_connection(port)
    flag = process_first_transmission(connection)
    if flag == 1: 
        # client side script is request.py
        print ("retrieving files...")
        retrieve = Retrieve(connection)              
        retrieve.process_request()
        print ("complete")
    elif flag == 2:
        # client side script is upload_more.py
        print ("uploading additional files...")
        store_more = StoreMore(connection)
        store_more.send_data()
        store_more.store_id_to_name_db()
        store_more.store_word_to_id_db(1)
        store_more.store_enc_files()
    else: 
        # client side script is upload.py
        print ("uploading files...")
        store = Store(connection)
        store.store_id_to_name_db()
        store.store_word_to_id_db()
        store.store_enc_files()
    connection.close()




