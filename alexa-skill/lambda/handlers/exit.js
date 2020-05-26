/* eslint-disable  func-names */
/* eslint-disable  no-console */

const ExitHandler = {
    canHandle(handlerInput) {
      return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent'
          || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent');
    },
    handle(handlerInput) {      
      console.log(`~~~~ Session ended: ${JSON.stringify(handlerInput.requestEnvelope)}`);
      return handlerInput.responseBuilder
        .getResponse();
    },
  };

module.exports = ExitHandler;