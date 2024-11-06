#!/bin/bash

# Generate CA certificate
openssl genpkey -algorithm RSA -out ca_key.pem
openssl req -x509 -new -key ca_key.pem -days 365 -out ca_cert.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=CA"

# Generate server key
openssl genpkey -algorithm RSA -out server_key.pem

# Generate server certificate signing request with SAN for localhost
openssl req -new -key server_key.pem -out server.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"

# Create a config file for SAN
echo "subjectAltName=DNS:localhost" > san.cnf

# Sign the server CSR with the CA, adding the SAN config
openssl x509 -req -in server.csr -CA ca_cert.pem -CAkey ca_key.pem -CAcreateserial -out server_cert.pem -days 365 -extfile san.cnf

# Generate client key and certificate
openssl genpkey -algorithm RSA -out client_key.pem
openssl req -new -key client_key.pem -out client.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=Client"
openssl x509 -req -in client.csr -CA ca_cert.pem -CAkey ca_key.pem -CAcreateserial -out client_cert.pem -days 365

# Clean up the SAN config file
rm san.cnf

echo "Certificate generation complete!"
