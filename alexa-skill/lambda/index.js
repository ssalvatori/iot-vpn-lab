'use strict';

const Alexa = require('ask-sdk-core');

const ErrorHandler = require('./handlers/error');
const ExitHandler = require('./handlers/exit');  //CancelIntent & StopIntent
const SessionEndedRequestHandler = require('./handlers/session_ended');
const HelpHandler = require('./handlers/help'); //HelpIntent
const ToCountryIntent = require('./handlers/to_country'); //ToCountryIntent
const LaunchRequestHandler = require('./handlers/launch_request'); //LaunchRequest

/* LAMBDA SETUP */
const skillBuilder = Alexa.SkillBuilders.custom();

exports.handler = skillBuilder
  .addRequestHandlers(
    LaunchRequestHandler,
    ToCountryIntent,
    HelpHandler,
    ExitHandler,
    SessionEndedRequestHandler,
  )
  .addErrorHandlers(ErrorHandler)
  .lambda();