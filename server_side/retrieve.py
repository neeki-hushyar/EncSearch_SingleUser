import server_imports
from server_imports import *


    
class Retrieve:
    def __init__(self, connection):
        self.server_connection = connection
        self.word_to_id = self._rtrv_word_to_id_map()

    def process_request(self):
        """
        Server accepts encrypted query and finds and returns files containing
        keyword.
        """
        buffer_size = self._get_buffer_size()
        enc_word = self.server_connection.recv(buffer_size)
        try:
            ids = self.word_to_id[enc_word]
        except KeyError:
            # code should never get this far unless dbs are out of sync
            # or user types in word that DNE
            print ("Word does not exist in any document on server.")
            sys.exit()
        id_to_name = self._rtrv_id_to_name_map()
        self.server_connection.send(self._int_to_binary(len(ids)).encode())
        for file_id in ids:
            enc_name = id_to_name[file_id]
            self.server_connection.send(self._int_to_binary(len(enc_name)).encode())
            self.server_connection.send(enc_name)
            with open(str(file_id), "rb") as enc_file:
                file_as_string = b"".join(enc_file.readlines())
            self.server_connection.send(self._int_to_binary(len(file_as_string)).encode())
            self.server_connection.send(file_as_string)

    def _int_to_binary(self, base_ten):
        # returns 30 binary number of base 10 input
        return '{0:030b}'.format(base_ten)

    def _get_buffer_size(self):
        """ Return 30 bit binary number as base 10 int """
        return int(self.server_connection.recv(30).decode(), 2)

    def _rtrv_word_to_id_map(self):
        # reads word_to_id.txt
        opened = open("word_to_id.txt", "r")
        return eval("".join(opened.readlines()))
    
    def _rtrv_id_to_name_map(self):
        # reads id_to_name.txt
        opened = open("id_to_name.txt", "r")
        return eval("".join(opened.readlines()))
    
