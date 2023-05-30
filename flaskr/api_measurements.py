import requests


def get_measurement_api(measurement_var: str):
    """
    return API measurement based on the measurement_var
    """
    api_url = f"http://fake_raspberry_api:80/measurements/{measurement_var}"
    response = requests.get(api_url, timeout=60)

    if measurement_var == "soil_moisture":
        soil_moisture = response.json()["Soil moisture"]
        return soil_moisture

    elif measurement_var == "acidity":
        acidity = response.json()["Acidity"]
        return acidity

    elif measurement_var == "lux":
        lux = response.json()["Lux"]
        return lux
