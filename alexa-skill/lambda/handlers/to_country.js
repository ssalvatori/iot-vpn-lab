'use strict';

var AWS = require('aws-sdk')

// eslint-disable-next-line no-undef
const ATS_ENDPOINT = process.env.ATS_ENDPOINT;
// eslint-disable-next-line no-undef
const THINGS_NAME = process.env.THINGS_NAME;;

const ToCountryIntent = {
    canHandle(handlerInput) {
      return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'ToCountryIntent';
    },
    handle(handlerInput) {  
      const countrySlot = handlerInput.requestEnvelope.request.intent.slots.country;

      let speakOutput = '';

      if (countrySlot && countrySlot.value) {
        console.log(`Country received ${countrySlot.value}`);

        let countryName = countrySlot.value.toLowerCase()
        speakOutput = `Sending message to change configuration to ${countryName}`;

        var iotdata = new AWS.IotData({endpoint:ATS_ENDPOINT});
        let topic = `$aws/things/${THINGS_NAME}/shadow/update`

        let state = {
          "state" : {
              "desired" : {
                  "country" : countryName,
               }
           }
        }
      
        var params = {
            topic: topic,
            payload: JSON.stringify(state),
            qos: 0
        };

        var request = iotdata.publish(params, function(err, data) {
            if(err){
                console.log(err);
            }
            else{
                console.log(`message ${JSON.stringify(state)} sent to ${topic}`)
            }
        });

      }

      return handlerInput.responseBuilder
        .speak(speakOutput)
        .getResponse();
    },
  };

module.exports = ToCountryIntent;