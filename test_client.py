import requests

url = "http://127.0.0.1:5000/predict"
payload = {
    "glucose": 130,
    "bmi": 27.5,
    "age": 45,
    "blood_pressure": 80
}

response = requests.post(url, json=payload)
print(response.json())
