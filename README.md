# AWS IoT + Alexa Skill + OpenVPN Integration (As A Code)

AWS IoT + Alex Skill + AWS Lambda + NordVPN + Rasperry PI WiFI Router

**Objective**: use *Amazon Alexa* to control a WiFi network secured by NordVPN, eveything should be done **As a Code**


Interactions:

* Alexa skill pushes a "country name" to an AWS IoT Shadow QUEUE (MQTT) [Check Alexa-Skill folder]
* Python daemon running in a Raspberry PI consumes mesage from th e AWS IoT Shadow QUEUE [Check Service folder], creates a new openvpn configuration with servers selected using the country provided and openvpn is restarted


## alexa-skill

* skill.json : amazon alexa skill definition

TODO: Alexa Skill should be creted as a code

## alexa-skill/lambda

NodeJS code to process Alexa Skill (this will be deployed by terraform/lambda)

## service

Python daemon to process messages sent by the alexa skill and restart openvpn with the new configuration

## terraform/lambda

Create AWS Lambda function to be use as alexa skill

## terraform/iot

Create AWS IoT Device

## terraform/lambda

Create AWS Lambda to be used by the Alexa Skill

## ansible

Setup raspberry pi (AP and OpenVPN installation)

* check configuration [ansible/README.md](ansible/README.md)
