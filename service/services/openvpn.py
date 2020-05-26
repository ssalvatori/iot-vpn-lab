import logging
import random
from datetime import datetime


class OpenvpnConfigurationError(Exception):
    """ Raised when there is an error creating the openvpn configuration """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'OpenvpnConfigurationError, {0} '.format(self.message)
        else:
            return 'OpenvpnConfigurationError has been raised'


class OpenvpnConfiguration:

    def __init__(self, configuration_path, country, transport, max_services=2, server_list_folder=None, credentials=None, template_dir="./"):
        """ OpenvConfiguration"""

        self.configuration_path = configuration_path
        self.template = "templates/openvpn.conf.j2"
        self.template_dir = template_dir
        self.max_services = max_services
        self.transport = transport
        self.country = country
        self.servers = []
        self.credentials = credentials
        self.server_list_folder = server_list_folder

    def get_servers(self):
        """ Read the server list from a given country """

        try:
            logging.info('Geting server for {} and path {}'.format(
                self.country, self.server_list_folder))

            serverlist = '{}/{}/servers_{}.txt'.format(
                self.server_list_folder, self.transport, self.country)

            with open(serverlist) as serverlist_file:
                self.servers = serverlist_file.readlines()

            if len(self.servers) < 1:
                raise ValueError('No servers found for that country')
            else:
                logging.info('found {} servers'.format(len(self.servers)))

        except ValueError as error:
            raise OpenvpnConfigurationError(
                'No servers found for {}'.format(self.country))
        except Exception as error:
            logging.error(str(error))
            raise OpenvpnConfigurationError('unexpected error')

    def generate(self):
        """ Generate openvpn configuration using template """

        try:
            from jinja2 import Template, FileSystemLoader, Environment

            templateLoader = FileSystemLoader(searchpath=self.template_dir)
            templateEnv = Environment(loader=templateLoader)
            template = templateEnv.get_template(self.template)

            logging.info(
                "Generating configuration from {}/{}".format(self.template_dir, self.template))

            random.shuffle(self.servers)

            outputText = template.render(
                transport=self.transport,
                servers=self.servers[0:self.max_services],
                credentials=self.credentials,
                country=self.country,
                now=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            )

            output_conf = "{}/nordvpn.conf".format(self.configuration_path)
            logging.info(
                "Writing openvpn configuration to {}".format(output_conf))
            text_file = open(output_conf, "w")
            text_file.write(outputText)
            text_file.close()

        except Exception as error:
            logging.error(str(error))
