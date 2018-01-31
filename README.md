### Encrypted Search

**Enclosed:**  
&emsp;&emsp;&emsp;server side implementation  
&emsp;&emsp;&emsp;client side implementation  
&emsp;&emsp;&emsp;example files which were sent to the server in /files dir  


**Dependencies:**  
&emsp;&emsp;&emsp;Python 3  
&emsp;&emsp;&emsp;PyCrypto 2.6.1

**Capabilities:**
* Encrypts data on a remote server to allow user to retrieve a file by its encrypted name or any other individual encrypted word that shows up in that file. 
*  Every file is remains encrypted on the remote server.
* Upon file request[s] the server uses an encrypted keyword dictionary database to locate the corresponding file[s].
* After request, user receives encrypted file names and the corresponding file contents to decrypts. 


**Characteristics:**
* Outside attacker or third party operator can never read the contents stored on remote server.
* Client is the only entity with access to symmetric key needed to encrypt/decrypt the content.
* User does not store encrypted keyword database after constructing and transmitting it to server. (=paper).
* User can upload additional files to already initialized storage structure. (~paper)
* Uses hash of each string as IV for encryption in database --- predictable but unique.
* Keyword database allows server to retrieve all document IDs containing encrypted keyword in single look up.
* Files + search terms encrypted before reaching server (independent of encrypted transmission)

**Command Line Inputs:**  
&emsp;&emsp;&emsp;For description of CLA: ‘\<module> -h’

&emsp;***server_script.py:***  
&emsp;&emsp;&emsp;python3 server_script.py -p <optional_port>

&emsp;***client_side:***  
&emsp;upload.py:  
&emsp;&emsp;python3 upload.py -i <remote_IP> -d <rel_path_to_dir_to_enc>

&emsp;request.py:  
&emsp;&emsp;python3 request.py -i <remote_IP> -w <search_term> -d <full_path_to_dest_dir> -p <optional_port>

&emsp;upload_more.py:  
&emsp;&emsp;python3 upload_more.py -i <remote_IP> -d <rel_path_to_dir_to_enc>

After each round of testing the following files must be deleted in order to run program again and restart the encrypted keyword database:   
&emsp;&emsp;&emsp;server_side/word_to_id.txt  
&emsp;&emsp;&emsp;server_side/name_to_id.txt  
&emsp;&emsp;&emsp;any document on the server side whose name is an integer (i.e. server_side/0 server_side/1)

