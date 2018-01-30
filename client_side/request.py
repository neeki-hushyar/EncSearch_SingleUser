import client_imports
from client_imports import *
from upload import connect # make connect cnetral!
from upload import read_all_data


class Request:
    def __init__(self, sym_key1, sym_key2, parameters, connection):
        self.sym_key1 = sym_key1
        self.sym_key2 = sym_key2
        self.client_connection = connection
        self.search_word = parameters["search_word"]
        self.directory = parameters["directory"]
        
    def _get_hash(self):
        """ Compute hash (used for IV) with search word as seed. """
        h = MD5.new()
        h.update(self.search_word.encode())
        return h.digest()

    def rtrv_files(self):
        """
        Handles requests of files containing encrypted search term from server. 
        Handles reception of files returned by the server.
        """
        iv = self._get_hash()
        cipher = AES.new(self.sym_key1, AES.MODE_CFB, iv)
        enc_word = iv + cipher.encrypt(self.search_word)
        try:
            self._request(enc_word)
            self._receive_files()
            self.client_connection.close()
        except:
            self.client_connection.send(self._int_to_binary(1048575).encode())
            print ("No matching file found. Closing connection")
        self.client_connection.close()

    def _request(self, enc_word):
        # the 30 bit binary w/ int value of 1 (below) is a flag requesting retrieval
        self.client_connection.send(self._int_to_binary(len(enc_word)).encode())
        self.client_connection.send(enc_word)

    def _receive_files(self):
        """
        Decrypts and stores all files returned by the server
        """
        number_of_files = self._get_buffer_size()
        names = list()
        for i in range(number_of_files):
            buffer_size = self._get_buffer_size()
            enc_name = self.client_connection.recv(buffer_size) 
            buffer_size = self._get_buffer_size()
            unwritten = buffer_size
            parts = list()
            while unwritten > 0:
                data = self.client_connection.recv(unwritten)
                parts.append(data)
                unwritten -= len(data)
            enc_file_contents = b"".join(parts)
            print ("{0} encrypted file received".format(i+1))
            names.append(self._decrypt(enc_name, enc_file_contents))
        print ("The following files have been decrypted: {0}".format(str(names)))
 
        
    def _decrypt(self, name, content):
        """
        Decrypts encrypted file name and encrypted file content using symmetric
        keys 1 and 2, respectively.
        """
        cipher1 = AES.new(sym_key1, AES.MODE_CFB, name[:16])
        plaintext_name = cipher1.decrypt(name)[16:].decode()
        cipher2 = AES.new(sym_key2, AES.MODE_CFB, content[:16])
        plaintext_content = cipher2.decrypt(content)[16:].decode()
        plaintext_name = plaintext_name.split("/")[-1]
        self._write_to_file(plaintext_name, plaintext_content)
        return plaintext_name

    def _write_to_file(self, plaintext_name, plaintext_content):
        with open(os.path.join(self.directory, plaintext_name), "w+") as write_to:
            write_to.write(plaintext_content)

    def _get_buffer_size(self):
        """ Return 30 bit binary number as base 10 int """
        return int(self.client_connection.recv(30).decode(), 2)

    def _int_to_binary(self, base_ten):
        return '{0:030b}'.format(base_ten)    


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='dest_ip')
    parser.add_argument('-w', dest='search_word')
    parser.add_argument('-p', dest='dest_port', default=9998)
    parser.add_argument('-d', dest='dir', default="",
                        help='directory to place retrieved files into')
    args = parser.parse_args()
    parameters = {"dest_ip":args.dest_ip, "dest_port":int(args.dest_port),
                  "search_word":args.search_word, "directory":args.dir}
    return parameters

def main():
    parameters = parse_arguments()
    connection = connect(parameters)
    # flag so server knows a retrieval is being requested
    start = time.time()
    connection.send(("0"*29 + "1").encode())
    request = Request(sym_key1, sym_key2, parameters, connection)
    request.rtrv_files()
    print ("Received in: {0} seconds".format(time.time()-start))


if __name__ == '__main__':
    main()
