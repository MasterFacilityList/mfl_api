import psycopg2

hostname = 'localhost'
username = 'mfl'
password = 'mfl'
database = 'mfl'

myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)