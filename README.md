# Secure File Transfer Project

 Intro to Computer Security COMP 2300\
 University of Massachusetts Lowell\
 Kennedy College of Sciences\
 Professor: Sashank Narain - Computer Science Department/Cybersecurity

### Authors:
Patricia Antlitz\
Andrew Jacobson\
Flower Letourneau\
Paul Warwick

---

## ATTENTION:

### To run the code:

The file that must be ran using `Makefile`

First, you will need to generate SSL/TLS certificates for mutual authentication:

for this to work properly, you will need to have OpenSSL installed

### UNIX and LINUX:

first, you must run the bash file generate_certificates.sh:

**run:**\
`./generate_certificates.sh` which contains all commands needed to generate the required certificates

OR `make generate-certificates`

### WINDOWS:

In this case, you will need to run the file generate_windows_cert.sh instead:

**run:**\
`./generate_windows_cert.sh` which contains all commands needed to generate the required certificates

OR `make generate-windows-cert`

NOTE: I do not have a windows machine so I was NOT abke to test this script. In fact, this one script was generated by AI and I dont know if it works. In case of failure, use a Unix or Linux device.

**if you are unable to run the bash file due to file restrictions, run:**
`chmod 755 generate_certs.sh`

---

### Virtual Environment:

In order to run bcrypt, you might need to set up a virtual environment:

Unix/Linux:

`python3 -m venv venv`

`source venv/bin/activate`

Windows:

`python3 -m venv venv`

`.\venv\Scripts\activate`

**DEACTIVATE:** `deactivate` once you are done

**then run:**\
`make install` to install dependencies from requirements.txt IF needed

---

### Run the program:

**run:**\
`make run` to run the program

**To clean (removes certificates and cleans cache):**\
`make clean`

Always use make clean to delete your local certificates

## ATTENTION:

### Avoid running `make` by itself

This code runs on port 8443

to kill it on unix systems, first find the port by running the following command:
`lsof -i :8443`

then kill it by:
`kill -9 <PID>`


---

## Objective:

This project is designed to introduce you to essential cryptographic tools by building a secure file-sharing protocol similar to Apple’s AirDrop. In completing this project, you will engage with fundamental concepts in cryptography and cybersecurity, such as symmetric and asymmetric encryption, digital certificates, public key infrastructure, mutual authentication, non-repudiation, confidentiality, integrity assurance, and password protection techniques.

This project aims to utilize cryptographic tools to implement a secure file transfer protocol.


## Version 1 - Milestone 1:

Project Milestone 1-3:

@version: 1.0.0.1 - initial commit - Project part 1\
@version: 1.1.2.5 - Milestone 1 basic user registration\
@version: 1.1.4.14 - bcrypt - Hashing\
@version: 1.1.5.1 - SSL/TLS certificates, RSA
@version: 1.2.2.1 - garbage collection
@version 1.3.1.1 - contact.py file added with basic implementation
@version 1.3.2.1 - implemented contact list for ADD only, connected to menu file

For Milestone 1-3 we have the following files

utils.py = shared functions for loading, reading and writing on the users.json file

users.json = list of users and contacts

user.py = user registration, and log in

encrypt.py = password hashing for encryption using bcrypt

menu_options = help options when the user successfully logsin - ADD fuctionality for now

contacts.py = adds a new contact to the current user logged in

mutual_cert.py = SSL certificates for login, sign up security

main.py = main fole, runs the code, garbage collection

Makefile = must be used to run this program


## Version 2 - Milestone 2

@version: 2.4.1.6 - files created for milestone 4:\
    for contacts.py = list function has been initialized and commented out for now\
    for menu_options.py = other menu options are there but commented out.

--- 

### Specs:

**Milestone 1 - User Registration**

When developing this module, keep the following in mind:

1. You don’t need a database; simple files, YAML, or JSON structures will work.
2. Begin by implementing the module without security controls. Once you confirm it’s working correctly, add security measures to guard against common password cracking attacks.
3. Focus on reusability in your code, especially for password protections that will also be useful in the User Login milestone.
4. Consider using third-party APIs, such as the Python `crypt` module, to create salted hashes for securing passwords.
5. During registration, generate and store information to support mutual authentication in future milestones. Using digital certificates will be possible if you assume a trusted Certificate Authority (CA) is available on all clients.

**Milestone 2 - User Login**

This milestone can be implemented quickly. Important points to keep in mind:

1. Reuse as much code as possible from the User Registration milestone.
2. Consider how login data can enhance security in future milestones. Store this data securely in memory during the session, and ensure that all information is erased from memory when the program exits.

**Milestone 3 - Adding Contacts**

This module is straightforward and should be relatively quick to implement. Key considerations:

1. A database isn’t necessary; using files, YAML, or JSON will suffice. Assume each user has a small number of contacts.
2. Utilize information generated in Milestone 2 to ensure that contact information remains confidential and intact. Protect against unauthorized access or tampering by malicious users.

---

# Data Security Layers:

1. **bcrypt for Password Hashing (Not Encryption/Decryption)**

bcrypt is a hashing algorithm. It is used to securely hash passwords for storage, which is a one-way process.\
Hashing with bcrypt ensures that even if someone gains access to our stored data (such as our JSON file), they cannot easily retrieve the original password, because hashes are irreversible.\
When a user registers, the password is hashed with bcrypt and then stored in the JSON file. During login, the entered password is hashed again and compared with the stored hash to verify the password.

Important Note: bcrypt does not encrypt or decrypt passwords. Instead, it’s used to securely store a hashed version of the password, protecting it from offline password-cracking attacks.

2. **SSL/TLS for Secure Transmission**

SSL/TLS provides a secure communication channel between the client and server by encrypting data during transmission. This prevents third parties from intercepting sensitive information, like passwords, as they travel over the network.\
Our code uses SSL/TLS to establish a mutual authentication connection with certificates on both the client and server sides. This ensures that both parties are verified and that all transmitted data is encrypted during transit.\
Data is decrypted only on the receiving end, so it remains encrypted while traveling between the client and server.

3. **Additional RSA Encryption for Password Transmission**

An extra layer of security was added: RSA encryption for the password on the client side using the server's public key before transmission.\
RSA encrypts the password on the client side (using the server’s public key), which is then transmitted over the already secure TLS connection.\
On the server side, the password is decrypted with the server’s private key to get back the original plaintext password, which is then passed through bcrypt for verification against the stored hash.


---

### Technologies Used:
Python\
GitHub\
Git\
Json\
Hashing by bcryot\
SSL\
TLS\
RSA

