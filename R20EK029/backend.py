from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

JOHN_DOE_R_API_URL = "http://104.211.219.98/train/register"
ACCESS_CODE = "MOJPate"


@app.route("/trains", methods=["GET"])
def get_train_schedules():
    current_time = datetime.now()
    end_time = current_time + timedelta(hours=12)

    headers = {
        "Authorization": f"Bearer {get_auth_token()}",
        "Accept": "application/json",
        "companyName": "Train Central",
        "ownerName": "SHASHANK",
        "rollNo": "R20EK029",
        "ownerEmail": "myselfshashankgowda@gmail.com",
        "accessCode": "MOJPate"
    }

    response = requests.get(
        r"http://104.211.219.98/train/trains", headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch train schedules"})

    trains = response.json().get("trains", [])

    available_trains = []
    for train in trains:
        departure_time = datetime.strptime(
            train["departure_time"], "%Y-%m-%d %H:%M:%S")
        if current_time <= departure_time <= end_time and departure_time >= current_time + timedelta(minutes=30):
            available_trains.append(train)

    available_trains.sort(key=lambda x: (
        x["price"], -x["seat_availability"], x["departure_time"]), reverse=False)

    return jsonify(available_trains)


def get_auth_token():
    payload = {
        "access_code": ACCESS_CODE,
        "rollNo": request.headers.get("R20EK029"),
        "companyName": "Train Central",
        "clientID": "b46118f0-fb16-4b16-a4b1-6ae6ad718b27",
        "ownerEmail": "myselfshashankgowda@gmail.com",
        "clientSecret": "XOyol0RPasKW0dAN",
    }

    response = requests.post(
        r"http://104.211.219.98/train/auth/", json=payload)
    if response.status_code == 200:
        return response.json().get("token", "")
    else:
        return ""


if __name__ == "__main__":
    app.run(debug=True, port=5005)
