from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import os
import pycountry

from services import openvpn
from services import systemd

# countries = [
#     'IT',
#     'CL',
#     'EE',
#     'DE',
#     'US',
#     'UK'
# ]


def proccessMessage(country_code, received_country):
    """ proccessMessage """

    try:
        # validCountry(country)
        conf = openvpn.OpenvpnConfiguration(
            configuration_path=nordvpn_configuration,
            country=country_code,
            transport=nordvpn_protocol,
            max_services=nordvpn_max_servers,
            server_list_folder=nordvpn_conf_pah,
            credentials=nordvpn_credentials,
            template_dir=nordvpn_template_dir
        )
        conf.get_servers()
        conf.generate()
        systemd.restart_service('openvpn@nordvpn.service')
        openvpn_service = systemd.is_service_running('openvpn')

        logging.info('Openvpn running: {}'.format(str(openvpn_service)))

        state = {
            'state': {
                'reported': {
                    'country': received_country
                }
            }
        }

        deviceShadowHandler.shadowUpdate(json.dumps(state), None, 5)

    except ValueError as error:
        logging.error(str(error))
    except openvpn.OpenvpnConfigurationError as error:
        logging.error(str(error))


# def validCountry(countryCode):
#     logging.info('Validating {}'.format(countryCode))
#     if countryCode.upper() in countries:
#         return True
#     else:
#         raise ValueError('country {} not valid'.format(countryCode))


def onDeltaMessage(payload, responseStatus, token):
    try:
        payloadDict = json.loads(payload)
        received_country = payloadDict['state']['country']
        country = pycountry.countries.search_fuzzy(received_country)
        if len(country) > 0:
            country_code = country[0].alpha_2
            logging.info("Country code: {}".format(country_code))
            proccessMessage(country_code.lower(), received_country)

    except AttributeError as error:
        logging.error('discarding message - '+str(error))


logger = logging.getLogger()
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


aws_root_ca = os.environ['AWS_ROOT_CA']
private_key = os.environ['AWS_THING_PRIVATE_KEY']
cert = os.environ['AWS_THING_CERT']
aws_ats_port = int(os.environ['AWS_THINS_ATS_PORT'])
aws_ats_endpoint = os.environ['AWS_THINS_ATS_ENDPOINT']
client_id = "1234"
thing_name = os.environ['AWS_THING_NAME']
nordvpn_conf_pah = os.environ['NORDVPN_CONFS_PATH']
nordvpn_credentials = os.environ['NORDVPN_CREDENTIALS']
nordvpn_configuration = os.environ['NORDVPN_CONF']
nordvpn_protocol = os.environ['NORDVPN_PROTOCOL']
nordvpn_max_servers = int(os.environ['NORDVPN_MAX_SERVERS'])
nordvpn_template_dir = os.environ['NORDVPN_TEMPLATE_DIR']

logging.info("** Start Configurations **")
logging.info("AWS_ROOT_CA {}".format(aws_root_ca))
logging.info("AWS_THING_PRIVATE_KEY {}".format(private_key))
logging.info("AWS_THING_CERT {}".format(cert))
logging.info("AWS_THINS_ATS_ENDPOINT {}".format(aws_ats_endpoint))
logging.info("AWS_THINS_ATS_PORT {}".format(aws_ats_port))
logging.info("AWS_THING_NAME {}".format(thing_name))
logging.info("NORDVPN_CONFS_PATH {}".format(nordvpn_conf_pah))
logging.info("NORDVPN_CONF {}".format(nordvpn_configuration))
logging.info("NORDVPN_PROTOCOL {}".format(nordvpn_protocol))
logging.info("NORDVPN_CREDENTIALS {}".format(nordvpn_credentials))
logging.info("NORDVPN_MAX_SERVERS {}".format(nordvpn_max_servers))
logging.info("NORDVPN_TEMPLATE_DIR {}".format(nordvpn_template_dir))
logging.info("** End Configurations **")


mqttc = AWSIoTMQTTShadowClient(client_id)
mqttc.configureEndpoint(aws_ats_endpoint, aws_ats_port)
mqttc.configureCredentials(aws_root_ca, private_key, cert)

mqttc.configureAutoReconnectBackoffTime(1, 32, 20)
mqttc.configureConnectDisconnectTimeout(10)
mqttc.configureMQTTOperationTimeout(5)

mqttc.connect()

deviceShadowHandler = mqttc.createShadowHandlerWithName(thing_name, True)
deviceShadowHandler.shadowRegisterDeltaCallback(onDeltaMessage)

while True:
    time.sleep(1)
