# Secure File Transfer Project

 Intro to Computer Security COMP 2300\
 University of Massachusetts Lowell\
 Kennedy College of Sciences\
 Professor: Sashank Narain - Computer Science Department/Cybersecurity

### Authors:
Andrew Jacobson  
Flower Letourneau  
Paul Warwick  
Patricia Antlitz

---

### To run the code:

THe file that must be ran using `Makefile`

First, you will need to generate SSL/TLS certificates for mutual authentication:

**run:**\
`./generate_certificates.sh` which contains all commands needed to generate the required certificates

**then run:**\
`make install` to install dependencies from requirements.txt

**and:88\
`make run` to run the program

**To clean (removes certificates and cleans cache):**\
`make clean`

---

## Objective:

This project is designed to introduce you to essential cryptographic tools by building a secure file-sharing protocol similar to Apple’s AirDrop. In completing this project, you will engage with fundamental concepts in cryptography and cybersecurity, such as symmetric and asymmetric encryption, digital certificates, public key infrastructure, mutual authentication, non-repudiation, confidentiality, integrity assurance, and password protection techniques.

This project aims to utilize cryptographic tools to implement a secure file transfer protocol.


## Version 1:

Project Milestone 1-3:

@version: 1.0.0.1 - initial commit - Project part 1\
@version: 1.1.2.5 - Milestone 1 basic user registration\
@version: 1.1.4.14 - bcrypt
@version: 1.1.5.1 - SSL/TLS certificates
- space holder for future part 1 versions

@version: 2.4.1.6 - files created for milestone 4

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

### Technologies Used:
Python\
GitHub\
Git\
Json\

