import random
import time
import sqlite3

db = sqlite3.connect('../instance/flaskr.sqlite')
db.row_factory = sqlite3.Row # returns row as dicts

def random_measurements(db):
    '''
    Commit to db new measurements every 10 sec
    '''

    while True:
        humidity = random.randrange(0,100)
        aciditiy = round(random.uniform(4,7),2)
        lux = random.randrange(1000,3000)
        print(humidity,aciditiy,lux)
        db.execute(
                'INSERT INTO  measurements (humidity, acidity, lux) VALUES (?,?,?) ',
                (humidity, aciditiy, lux))
        db.commit()
        time.sleep(10.0)

random_measurements(db)
