# Makefile runs this code

# variables
PYTHON = python3
PIP = pip3

# Targets
.PHONY: all install generate_certificates generate_windows_cert run clean

all: install generate-certificates run

# install dependencies
install:
	$(PIP) install -r requirements.txt

# generate certificates
generate_certificates:
	./generate_certificates.sh
generate_windows_cert:
	./generate_windows_cert

# Run application
run:
	$(PYTHON) src/main.py

# Clean up generated certificates and other files
clean:
	rm -rf certs
	rm -rf src/__pycache__
