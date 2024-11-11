# Makefile runs this code

# variables
PYTHON = python3
PIP = pip3

# Targets
.PHONY: all install generate-certificates run clean

all: install generate-certificates run

# install dependencies
install:
	$(PIP) install -r requirements.txt

# generate certificates
generate_certificates:
	./generate_certificates.sh

# Run application
run:
	$(PYTHON) src/main.py

# Clean up generated certificates and other files
clean:
	rm -rf certs
	rm -rf src/__pycache__
