# Makefile runs this code

# variables
PYTHON = python3
PIP = pip3

# Targets
.PHONY: all install generate-certificates generate-windows-cert run clean

# install dependencies
install:
	$(PIP) install -r requirements.txt

# generate certificates
generate-certificates:
	./generate_certificates.sh
generate-windows-cert:
	./generate_windows_cert

# Run application
run:
	$(PYTHON) src/main.py

# Clean up generated certificates and other files
clean:
	rm -rf certs
	rm -rf src/__pycache__
