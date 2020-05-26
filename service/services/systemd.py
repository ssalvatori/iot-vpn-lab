import dbus
import logging
from dbus import SystemBus


def is_service_running(service):
    """ Queries systemd through dbus to see if the service is running """
    service_running = False
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    try:
        service_unit = service if service.endswith('.service') else manager.GetUnit("{}.service".format(service))
        service_proxy = bus.get_object('org.freedesktop.systemd1', str(service_unit))
        service_properties = dbus.Interface(service_proxy, dbus_interface='org.freedesktop.DBus.Properties')
        service_load_state = service_properties.Get('org.freedesktop.systemd1.Unit', 'LoadState')
        service_active_state = service_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
        if service_load_state == 'loaded' and service_active_state == 'active':
            service_running = True
    except dbus.DBusException as error:
        logging.error(str(error))

    return service_running

def restart_service(service):
    """ Restart systemd service using through """
    try:
        bus = SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
        service_unit = service_unit = service if service.endswith('.service') else manager.GetUnit("{}.service".format(service))
        logging.info('Restarting {}'.format(service_unit))
        manager.TryRestartUnit(service_unit, 'replace')
    except dbus.DBusException as error:
        logging.error(str(error))


def stop_service(service):
    """ Stop systemd service using through """
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    try:
        service_unit = service if service.endswith('.service') else manager.GetUnit("{}.service".format(service))
        manager.StopUnit(service_unit, 'replace')
    except dbus.DBusException as error:
        logging.error(str(error))

def start_service(service):
    """ Start systemd service using through """
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    try:
        service_unit = service if service.endswith('.service') else manager.GetUnit("{}.service".format(service))
        manager.StartUnit(service_unit, 'replace')
    except dbus.DBusException as error:
        logging.error(str(error))