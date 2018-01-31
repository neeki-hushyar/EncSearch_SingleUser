Encrypted Search in Simulated Cloud 

**Enclosed:**
	server side implementation
	client side implementation
	example files which were sent to the server in /files dir

**Dependencies:**
	Python 3
	PyCrypto 2.6.1

**Capabilities:**
This is a simulation which encrypts data on a remote server in such way
that a user can retrieve a file by it's encrypted name or any other single 
encrypted word that shows up in that file. Every file is encrypted on the
remote server and the server uses an encrypted keyword dictionary database
to locate the corresponding file[s] to return to the user. The user receives
encrypted file names and the corresponding file content and decrypts it. This is designed in such way that an outside attacker can never read the contents stored in addition to the third party operated itself. This is because the client is the only entity which ever knows the symmetric key which is used to encrypt/decrypt the content.

**Characteristics:**
- user never stores encrypted keyword database after it constructs and sends it to the server (similar in concept but not implementation as the design in the paper)
- user can upload additional files to already initialized storage structure (not possible in paper - static storage only)
- user sends single encrypted query to server upon request (different from paper which sent as many encrypted queries as documents bc of problems with the IV, these problems and my solution are addressed in the paper)
- implementation of keyword database allows server to retrieve all document ids containing encrypted keyword in single look up (as a result of previous characteristic)

**Command Line Inputs:**
for info about command line arguments type ‘module_name.py -h’

**server_script.py:**
  python3 server_script.py -p <optional_port>

**client_side:**
upload.py:
  python3 upload.py -i <remote_IP> -d <rel_path_to_dir_to_enc>
  
request.py:
  python3 request.py -i <remote_IP> -w SEARCH_TERM -d <full_path_to_dest_dir> -p <optional_port>

upload_more.py:
  python3 upload_more.py -i <remote_IP> -d <rel_path_to_dir_to_enc>

After each round of testing the following files must be deleted in order to run program again and restart the encrypted keyword database: 
	server_side/word_to_id.txt
	server_side/name_to_id.txt
	any document on the server side whose name is an integer: 
		i.e. server_side/0 server_side/1
