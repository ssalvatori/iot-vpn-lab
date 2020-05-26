/* eslint-disable  func-names */
/* eslint-disable  no-console */

const ErrorHandler = {
    canHandle() {
      return true;
    },
    handle(handlerInput, error) {
      console.log(`Error handled: ${error.message}`);
  
      return handlerInput.responseBuilder
        .speak('Sorry, I can\'t understand the command. Please say again.')
        .getResponse();
    },
  };

module.exports = ErrorHandler;