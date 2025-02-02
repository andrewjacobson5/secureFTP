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

### Server start

**run:**\
`python3 src/tls_server.py` to run the tls server

Then open a new terminal once server is up...

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

### Technologies Used:
Python\
GitHub\
Git\
Json\
Hashing by bcrypt\
SSL\
TLS\
RSA

