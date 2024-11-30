#!/bin/bash

mkdir -p certs

# Generate CA certificate with key usage
openssl genpkey -algorithm RSA -out certs/ca_key.pem
openssl req -x509 -new -key certs/ca_key.pem -days 365 -out certs/ca_cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=CA" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"

# Generate server key and certificate with SAN
openssl genpkey -algorithm RSA -out certs/server_key.pem
openssl req -new -key certs/server_key.pem -out certs/server.csr \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"
openssl x509 -req -in certs/server.csr -CA certs/ca_cert.pem -CAkey certs/ca_key.pem -CAcreateserial \
  -out certs/server_cert.pem -days 365 \
  -extfile <(printf "subjectAltName=DNS:localhost,IP:127.0.0.1\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth")

# Generate client key and certificate
openssl genpkey -algorithm RSA -out certs/client_key.pem
openssl req -new -key certs/client_key.pem -out certs/client.csr \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=Client"
openssl x509 -req -in certs/client.csr -CA certs/ca_cert.pem -CAkey certs/ca_key.pem -CAcreateserial \
  -out certs/client_cert.pem -days 365 \
  -extfile <(printf "keyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=clientAuth")

echo "Certificates generated successfully!"
