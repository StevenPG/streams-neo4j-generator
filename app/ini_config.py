from configparser import ConfigParser

from app.scan import ScannerConfiguration

config = ConfigParser()


def scan_configuration() -> ScannerConfiguration:
    """
    Get the contents of the Configuration .ini file and return to caller
    TODO - need to allow overriding via CLI
    :return: contents of .ini file
    """
    config.read(filenames='config.ini')
    return ScannerConfiguration(config)
