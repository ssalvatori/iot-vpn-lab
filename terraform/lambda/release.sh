#!/bin/bash

set -x

BASE="${PWD}"

LAMBDA_FUNCTION="../../alexa-skill/lambda"
cd ${LAMBDA_FUNCTION} && rm -rf ../../../lamdba.zip && npm install
zip -r ${BASE}/lamdba.zip index.js node_modules handlers package.json utils.js package-lock.json -x '*.DS_Store'