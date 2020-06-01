import os

PASS = os.environ.get('MYSQL_PASS')

databaseURI = f'mysql://root:{PASS}@localhost/test'
