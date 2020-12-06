import mysql.connector

class UseDatabase:
    
    def __init__(self, config: dict):
        self.configuration = config

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
            
        except  mysql.connector.errors.InterfaceError as err:
            raise ConnectorError(err)
            
        except  mysql.connector.errors.ProgrammingError as err:
            raise CredentialError(err)
            
    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
        if exception_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exception_value)
        
class ConnectorError(Exception):
    pass
    
class CredentialError(Exception):
    pass
    
class SQLError(Exception):
    pass
