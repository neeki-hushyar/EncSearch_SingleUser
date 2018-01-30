import server_imports
from server_imports import *
import store
from store import *



class StoreMore(Store):
    def __init__(self, connection):
        super().__init__(connection)
        self.map_id_to_name = None
        self.word_to_id = self._rtrv_word_to_id_map()

    def send_data(self):
        """
        Send to client the lowerbound of integers to begin assigning
        the new document IDs. Send id to name db.
        """
        self._rtrv_id_to_name_map()
        ids = [int(x) for x in self.map_id_to_name.keys()]
        lower_bound = max(ids) + 1
        self.server_connection.send(self._int_to_binary(lower_bound).encode())
        self.server_connection.send(self._int_to_binary(len(str(self.map_id_to_name))).encode())
        self.server_connection.send(str(self.map_id_to_name).encode())
        
    def _rtrv_id_to_name_map(self): 
        opened = open("id_to_name.txt", "r")
        self.map_id_to_name = eval("".join(opened.readlines()))

    def _rtrv_word_to_id_map(self):
        opened = open("word_to_id.txt", "r")
        return eval("".join(opened.readlines()))

    
