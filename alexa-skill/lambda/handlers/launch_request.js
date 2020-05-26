'use strict';
var AWS = require('aws-sdk');

// eslint-disable-next-line no-undef
const ATS_ENDPOINT = process.env.ATS_ENDPOINT;
// eslint-disable-next-line no-undef
const THINGS_NAME = process.env.THINGS_NAME;

const LaunchRequestHandler = {
    canHandle(handlerInput) {
      return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    handle(handlerInput) {

      var iotdata = new AWS.IotData({endpoint:ATS_ENDPOINT});
      let topic = `$aws/things/${THINGS_NAME}/shadow/update`

      let state = {
        "state" : {
            "desired" : {
                "country" : "",
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
              console.log(`message ${JSON.stringify(state)} sent to ${topic}`);
          }
      });

      request.send()
  
      let speakOutput = `To use this skill please say: alexa tell vpn lab connect to country`;

      return handlerInput.responseBuilder
        .speak(speakOutput)
        .getResponse();
    },
  };

module.exports = LaunchRequestHandler;