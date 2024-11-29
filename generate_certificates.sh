#!/bin/bash

# Create the certs directory if it doesn't exist
mkdir -p certs

# Generate CA certificate
openssl genpkey -algorithm RSA -out certs/ca_key.pem
openssl req -x509 -new -key certs/ca_key.pem -days 365 -out certs/ca_cert.pem -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=CA"

# Generate server key
openssl genpkey -algorithm RSA -out certs/server_key.pem

# Generate server certificate signing request with SAN for localhost
openssl req -new -key certs/server_key.pem -out certs/server.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"

# Create a config file for SAN # Upadate 11/29 added IP for localhost testing. 
cat << EOF > san.cnf
subjectAltName=DNS:localhost,IP:127.0.0.1
EOF

# Sign the server CSR with the CA, adding the SAN config
openssl x509 -req -in certs/server.csr -CA certs/ca_cert.pem -CAkey certs/ca_key.pem -CAcreateserial -out certs/server_cert.pem -days 365 -extfile san.cnf

# Generate client key and certificate
openssl genpkey -algorithm RSA -out certs/client_key.pem
openssl req -new -key certs/client_key.pem -out certs/client.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=Client"
openssl x509 -req -in certs/client.csr -CA certs/ca_cert.pem -CAkey certs/ca_key.pem -CAcreateserial -out certs/client_cert.pem -days 365

# Clean up the SAN config file
rm san.cnf

echo "Certificate generation complete!"
