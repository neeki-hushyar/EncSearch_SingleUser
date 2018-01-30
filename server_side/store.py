import server_imports
from server_imports import *
import retrieve



class Store:
    def __init__(self, connection):
        self.server_connection = connection

    def write_data_to_file(self, buffer_size, file_name, enc_file = 0, additional=0):
        """ Writes data to specific file. If the content is not meant to be decoded
        it will not be. """
        unwritten = buffer_size
        parts = list()
        while unwritten > 0:
            data = self.server_connection.recv(unwritten)
            parts.append(data)
            unwritten -= len(data)
        if enc_file == 1:
            # enc file cannot be decoded
            enc_file_contents = b"".join(parts)
            opened = open(file_name, "wb+")
            opened.write(enc_file_contents)
        else:
            # dictionaries require decode()
            dictionary = b"".join(parts).decode()
            opened = open(file_name, "w")
            if additional:
                evaluated = eval(dictionary)
                for k, v in evaluated.items():
                    if k in self.word_to_id:
                        self.word_to_id[k] = self.word_to_id[k].union(v)
                    else:
                        self.word_to_id[k] = v
                opened.write(str(self.word_to_id))
            else:
                x = eval(dictionary)
                opened.write(dictionary)
        opened.close()

    def store_id_to_name_db(self):
        buffer_size = self._get_buffer_size()
        self.write_data_to_file(buffer_size, "id_to_name.txt")

    def store_word_to_id_db(self, additional=0):
        buffer_size = self._get_buffer_size()
        self.write_data_to_file(buffer_size, "word_to_id.txt", 0, additional)

    def store_enc_files(self):
        # stores encrypted files on server side
        number_of_files = self._get_buffer_size() # in this case returns # of files
        print ("{0} file[s] stored".format(number_of_files))
        for i in range(number_of_files):
            buffer_size = self._get_buffer_size()
            enc_name = self.server_connection.recv(buffer_size).decode()  
            buffer_size = self._get_buffer_size()
            self.write_data_to_file(buffer_size, enc_name, 1)
        self.server_connection.close()
    
    def _int_to_binary(self, base_ten):
        # converts base 10 integer into 30 bit binary integer
        return '{0:030b}'.format(base_ten)
 
    def _get_buffer_size(self):
        """ Return 30 bit binary number of buffer size as base 10 int """
        return int(self.server_connection.recv(30).decode(), 2)




