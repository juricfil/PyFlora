import random
import time
from flaskr.db import Measurements, db

def random_measurements():
    '''
    Commit to db new measurements every 10 sec
    '''

    while True:
        soil_moisture = random.randrange(0, 100)
        acidity = round(random.uniform(4, 7), 2)
        lux = random.randrange(1000, 3000)
        print(soil_moisture, acidity, lux)
        
        measurement = Measurements(soil_moisture=soil_moisture, acidity=acidity, lux=lux)
        db.session.add(measurement)
        db.session.commit()
        
        time.sleep(10.0)

random_measurements()
