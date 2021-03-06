__author__ = "Pruthvi Kumar"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

from configparser import ConfigParser
from configuration import ProtonConfig
from nucleus.generics.log_utilities import LogUtilities


class ConnectionDialects(ProtonConfig, LogUtilities):
    """
    One stop shop to get connectivity to any RDMBS for models.
    Current implementation covers:
    1. Postgres
    2. MySql
    3. SQL Server

    To add more support, add supporting config parameters into databaseConfig.ini file.

    NOTE: ConnectionDialect is reliant on databaseConfig.ini to establish valid connection. Please ensure
    you don't delete any existing config parameters.
    """
    def __init__(self):
        super(ConnectionDialects, self).__init__()
        self.logger = self.get_logger(log_file_name='connectionDialects_logs',
                                      log_file_path='{}/trace/connectionDialects_logs.log'.format(self.ROOT_DIR))
        self.dialect_store = self._config_store_parser

    def _config_store_parser(self):
        """
        Parse config file and prepare dialects for db supported by PROTON.
        By default PROTON ships with support for postgresql, mysql and sqlserver.
        :return: db Dialect
        """
        supported_databases = ['postgresql', ]  # v0.0.1 starts with support for pg.
        parser = ConfigParser()
        config_file = '{}/databaseConfig.ini'.format(self.ROOT_DIR)
        db = {}
        parser.read(config_file)

        def get_parsed_parameters(db_dialect, section):
            """
            Parser for databaseConfig.ini
            :param db_dialect: supported db dialects by PROTON.
            :param section: supported db name.
            :return: db dialect
            """

            if parser.has_section(section):
                db_dialect[section] = {}
                params = parser.items(section)
                for param in params:
                    db_dialect[section][param[0]] = param[1]
            else:
                self.logger.exception('[ConnectionDialects]: Section {} is not found in "databaseConfig.ini" '
                                 'file.'.format(section))
                raise Exception('[ConnectionDialects]: Section {} is not found in "databaseConfig.ini" '
                                'file.'.format(section))
            return db_dialect

        list(map(lambda sdb: get_parsed_parameters(db, sdb), supported_databases))
        return db


if __name__ == '__main__':
    cdl = ConnectionDialects()
    print(cdl.dialect_store())
