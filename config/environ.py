import os
import dotenv

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

class Environ:
    # Redshift 접속 정보
    REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
    REDSHIFT_USERNAME = os.getenv('REDSHIFT_USERNAME')
    REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
    REDSHIFT_DATABASE = os.getenv('REDSHIFT_DATABASE')