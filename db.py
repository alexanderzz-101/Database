import mysql.connector
import configparser

def get_connection():
    config = configparser.ConfigParser()
    config.read('config.ini')

    db = mysql.connector.connect(
        host=config['mysql']['host'],
        user=config['mysql']['user'],
        password=config['mysql']['password'],
        database=config['mysql']['database']
    )
    return db
