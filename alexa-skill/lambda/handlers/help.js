/* eslint-disable  func-names */
/* eslint-disable  no-console */

const HelpHandler = {
    canHandle(handlerInput) {
      return handlerInput.requestEnvelope.request.type === 'IntentRequest'
        && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {

      const speakOutput = handlerInput.t('HELP_MSG');
      
      return handlerInput.responseBuilder
        .speak(speakOutput)
        .reprompt(speakOutput)
        .getResponse();
    },
  };

module.exports = HelpHandler;