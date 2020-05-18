# AWS IoT + Alexa Skill + OpenVPN Integration (As A Code)

AWS IoT + Alex Skill + AWS Lambda + NordVPN + Rasperry PI WiFI Router

**Objective**: use *Amazon Alexa* to control a vpn network, eveything should be done **As a Code**

## alexa-skill

* skill.json : amazon alexa skill definition

TODO: Alexa Skill should be creted as a code

## alexa-skill/lambda

NodeJS code to process Alexa Skill (this will be deployed by terraform/lambda)

## service

Python daemon to process messages sent by the alexa skill

## terraform/lambda

Create AWS Lambda function to be use as alexa skill

## terraform/iot

Create AWS IoT Device

## terraform/lambda

Create AWS Lambda to be used by the Alexa Skill

## ansible

Setup raspberry pi (AP and OpenVPN installation)

* check configuration [ansible/README.md](ansible/README.md)
