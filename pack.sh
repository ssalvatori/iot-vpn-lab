#!/bin/bash

# Create a zip package with the python code to be deploy by ansible

BASE="${PWD}"

cd ${BASE}/service
zip -r ${BASE}/ansible/files/iot_vpn_lab.zip run.py requirements.txt services/*.py templates/*.j2
