import client_imports
from client_imports import *
import upload
from upload import *
import time


class UploadMore(Upload):
    def __init__(self, sym_key1, sym_key2, parameters, connection):
        super().__init__(sym_key1, sym_key2, parameters, connection)
        self.client_connection.send(self._int_to_binary(2).encode())

    def setup_keyword_db(self):
        # method override to ADD to setup keyword db, not start from scratch
        self.files = self._obtain_documents() # parent class method
        unencrypted_mapping = defaultdict(set)
        lower_bound = self._obtain_lb_id()
        self._write_id_to_name_map()
        for file_name in self.files:
            enc_name = self._encrypt_data(0, file_name)
            self.enc_names.append(str(lower_bound))
            self.map_id_to_name[lower_bound] = enc_name
            with open(file_name, "r") as content:
                if not file_name.endswith(".txt"):
                    continue
                for line in content.readlines():
                    for word in line.split(" "):
                        unencrypted_mapping[word].add(lower_bound)
        self._add_new_mappings(unencrypted_mapping)
    
    def _obtain_lb_id(self):
        # requests next number that will be assigned to document by server
        return self._get_buffer_size()
    
    def _write_id_to_name_map(self):
        buffer_size = self._get_buffer_size()
        self.map_id_to_name = eval(self.client_connection.recv(buffer_size).decode())
                              
    def _add_new_mappings(self, unenc_map):
        for unenc_word,ids in unenc_map.items():
            flag = 0
            iv = self._get_hash(unenc_word)
            cipher = AES.new(self.sym_key1, AES.MODE_CFB, iv)
            enc_word = iv + cipher.encrypt(unenc_word)
            if enc_word in self.map_word_to_id.keys():
                self.map_word_to_id[enc_word] = self.map_word_to_id[enc_word].union(ids)
                flag = 1
            if not flag:
                self.map_word_to_id[self._encrypt_data(0, unenc_word)] = ids

    def _get_buffer_size(self):
        """ Return 30 bit binary number as base 10 int """
        return int(self.client_connection.recv(30).decode(), 2)


def main():
    parameters = parse_arguments()
    connection = connect(parameters)
    start = time.time()
    upload_more = UploadMore(sym_key1, sym_key2, parameters, connection)
    upload_more.setup_keyword_db()
    upload_more.send_data()
    print ("Upload complete in {0} sec".format(time.time()-start))
    connection.close()


if __name__ == '__main__':
    main()
