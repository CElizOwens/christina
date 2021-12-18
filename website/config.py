import os
from flask_cors import CORS, cross_origin

PASS = os.environ.get('MYSQL_PASS')
SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key-goes-here"
SERVER_NAME = os.environ.get("APP_HOST")

databaseURI = f'mysql+mysqldb://root:{PASS}@localhost/opus'
test_databaseURI =  os.environ.get("JAWSDB_URL", f'mysql+mysqldb://root:{PASS}@localhost/test_opus')

cors = CORS()
cross_origin = cross_origin
