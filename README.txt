Encrypted Search in Simulated Cloud 

Enclosed:
	server side implementation
	client side implementation
	pycrypto tar library (third party library)
	example files which were sent to the server in /files dir

Required:
	Python3

Capabilities:

This is a simulation which encrypts data on a remote server in such way
that a user can retrieve a file by it's encrypted name or any other single 
encrypted word that shows up in that file. Every file is encrypted on the
remote server and the server uses an encrypted keyword dictionary database
to locate the corresponding file[s] to return to the user. The user receives
encrypted file names and the corresponding file content and decrypts it. This is designed in such way that an outside attacker can never read the contents stored in addition to the third party operated itself. This is because the client is the only entity which ever knows the symmetric key which is used to encrypt/decrypt the content.

characteristics (* denotes new design):
- user never stores encrypted keyword database after it constructs and sends it to the server (similar in concept but not implementation as the design in the paper)
* - user can upload additional files to already initialized storage structure (not possible in paper - static storage only)
* - user sends single encrypted query to server upon request (different from paper which sent as many encrypted queries as documents bc of problems with the IV, these problems and my solution are addressed in the paper)
* - implementation of keyword database allows server to retrieve all document ids containing encrypted keyword in single look up (as a result of previous characteristic)
