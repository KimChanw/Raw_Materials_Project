import redshift_connector
from config.environ import Environ

class RedshiftSession:
    @classmethod
    def redshift_connection(cls):
        conn = redshift_connector.connect(
            host=Environ.REDSHIFT_HOST,
            database=Environ.REDSHIFT_DATABASE,
            port=5439,
            user=Environ.REDSHIFT_USERNAME,
            password=Environ.REDSHIFT_PASSWORD
        )
        
        return conn.cursor()
