"""
This module encrypts data in folder and sends it destination.

Note: This module sends encrypted keyword database and encrypted document
(title and content). This module does NOT retreive symmetric key from TTP,
does not send the data over a secure connection (SSL) and does not deal with
access control aka authenticating a user has authroization to access the remote
server. AKA this project concerns encrypted search, and relies on implementation
of appropriate key management, access control and data in motion encryption.

"""
import client_imports
from client_imports import *



def connect(parameters):
    try:
        client_connection = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM)
        client_connection.connect((parameters["dest_ip"],
                                   parameters["dest_port"]))
        return client_connection
    except Exception as e:
        print (e)
        sys.exit()

class Upload:
    def __init__(self, sym_key1, sym_key2, parameters, connection):
        self.sym_key1 = sym_key1
        self.sym_key2 = sym_key2
        self.map_id_to_name = dict()
        self.map_word_to_id = defaultdict(set)
        self.client_connection = connection
        self.parameters = parameters
        self.files = list()
        self.enc_names = list()


    def _obtain_documents(self):
        """
        Returns list of txt files in directory specified by user.
        """
        dir = self.parameters["directory"]
        files = []
        for name in os.listdir(dir):
            full_path = os.path.join(dir, name)
            if os.path.isfile(full_path) and full_path.endswith(".txt"):
                files.append(full_path)
        return files 
    
    def setup_keyword_db(self):
        """
        Sets up a keyword database and id to name database
        """
        self.files = self._obtain_documents() 
        unencrypted_mapping = defaultdict(set)
        lower_bound = 0
        for file_name in self.files:
            enc_name = self._encrypt_data(0, file_name)
            # storing by id makes enc files easier to retrieve on server side
            self.enc_names.append(str(lower_bound))
            self.map_id_to_name[lower_bound] = enc_name
            with open(file_name, "r") as content:
                if not file_name.endswith(".txt"):
                    continue
                for line in content.readlines():
                    for word in line.split(" "):
                        # add words without puntutation (redundancy added)
                        # consider adding words lower case (redundancy added)
                        unencrypted_mapping[word].add(lower_bound)
            for word in unencrypted_mapping.keys():
                self.map_word_to_id[self._encrypt_data(0, word)] = unencrypted_mapping[word]
            # add encrypted file name to keyword db
            self.map_word_to_id[enc_name].add(lower_bound)
            lower_bound += 1
        # easier for server to read+write
        #self.map_word_to_id = dict(self.map_word_to_id)

    def _get_word_to_id_map(self):
        buffer_size = self._get_buffer_size()
        return eval(read_all_data(buffer_size, self.client_connection))

    def _get_hash(self, content):
        # the return value is used as an IV for the encryption of the search
        # word specified in the content variable
        h = MD5.new()
        h.update(content.encode())
        return h.digest()

    def _encrypt_data(self, flag, content):
        """ If flag == 0 -> encrypting file name/single term, 
            if flag == 1 -> encrypting file """
        iv = Random.new().read(AES.block_size) # new IV every encrypt        
        if flag == 0:
            iv = self._get_hash(content)
        sym_key = self.sym_key1
        if flag:
            sym_key = self.sym_key2
        cipher = AES.new(sym_key, AES.MODE_CFB, iv)
        return iv + cipher.encrypt(content)

    def _encrypt_file(self, file_name):
        print ("Encrypting {0}".format(file_name))
        file_as_string = open(file_name, "r").read()
        return self._encrypt_data(1, file_as_string)
    
    def _int_to_binary(self, base_ten):
        return '{0:030b}'.format(base_ten)
        
    def _send_maps(self):
        """
        Send size of map_id_to_name dict, dict, size of map_word_to_id dict, dict
        to server (order matters).
        """
        self.map_word_to_id = dict(self.map_word_to_id) # THIS SHOULD FIX EVERYTHING
        self.client_connection.send(self._int_to_binary(len(str(self.map_id_to_name))).encode())        
        id_to_name = str(self.map_id_to_name).encode()
        while len(id_to_name) > 0:
            self.client_connection.send(id_to_name[:1024])
            id_to_name = id_to_name[1024:]

        self.client_connection.send(self._int_to_binary(len(str(self.map_word_to_id))).encode())
        word_to_id = str(self.map_word_to_id).encode()
        while len(word_to_id) > 0:
            self.client_connection.send(word_to_id[:1024])
            word_to_id = word_to_id[1024:]

    def _send_files(self):
        """
        Send number of files, for each file send length of name, name, length of 
        file, file (order matters). Files are encrypted in this function so that
        they don't have to be enc all at once but one at a time and then forgotten.
        """
        print ("Sending files.")
        self.client_connection.send(self._int_to_binary(len(self.files)).encode())
        for enc_name, file in zip(self.enc_names, self.files):
            self.client_connection.send(self._int_to_binary(len(enc_name)).encode())
            if isinstance(enc_name, str):
                enc_name = enc_name.encode()
            self.client_connection.send(enc_name)
            enc_file = self._encrypt_file(file)
            self.client_connection.send(self._int_to_binary(len(enc_file)).encode())
            while len(enc_file) > 0:
                self.client_connection.send(enc_file[:1024])
                enc_file = enc_file[1024:]

    def send_data(self):
        self._send_maps()
        self._send_files()
        self.client_connection.close()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='dest_ip')
    parser.add_argument('-p', dest='dest_port', default=9998)
    parser.add_argument('-d', dest='directory')
    args = parser.parse_args()
    parameters = {"dest_ip":args.dest_ip, "dest_port":int(args.dest_port),
                  "directory":args.directory}
    return parameters


def main():
    parameters = parse_arguments()
    connection = connect(parameters)
    connection.send(("0"*30).encode()) # flag that this is upload
    start = time.time()
    upload = Upload(sym_key1, sym_key2, parameters, connection)
    upload.setup_keyword_db()
    upload.send_data()
    print ("Data sent. Connection Closed.\n{0} seconds".format(time.time()-start))


def read_all_data(buffer_size, connection):
    unwritten = buffer_size
    parts = list()
    while unwritten > 0:
        data = connection.recv(unwritten)
        parts.append(data)
        unwritten -= len(data)
    return b"".join(parts).decode()

if __name__ == '__main__':
    main()

    

    







