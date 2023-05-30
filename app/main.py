from fastapi import FastAPI
import random

app = FastAPI()


@app.get("/measurements/{measurement_type}")
async def measurement_generator(measurement_type: str) -> dict:
    """
    Generate different types of measurements and send them over api
    """
    if measurement_type == "soil_moisture":
        value = random.randrange(0, 100)
        return {"Soil moisture": value}
    elif measurement_type == "acidity":
        value = round(random.uniform(4, 7), 2)
        return {"Acidity": value}
    elif measurement_type == "lux":
        value = random.randrange(1000, 3000)
        return {"Lux": value}
    else:
        return {"error": "invalid measurement type"}
