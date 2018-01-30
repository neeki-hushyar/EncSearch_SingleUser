import Crypto
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
import sys
import os
import socket
import argparse
import time # testing ONLY   
import collections
from collections import defaultdict

sym_key1 = MD5.new(b'16BYTEKEY1').hexdigest()
sym_key2 = MD5.new(b'16BYTEKEY2').hexdigest()
