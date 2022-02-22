import requests
import datetime as dt
import smtplib
import time as t

MY_LONGITUDE = 88.141279
MY_LATITUDE = 25.022020


def check_coordinates(sat_longi, sat_lati):
    global MY_LONGITUDE, MY_LATITUDE
    if MY_LONGITUDE - 5 <= sat_longi <= MY_LONGITUDE + 5 and MY_LATITUDE - 5 <= sat_lati <= MY_LATITUDE + 5:
        return True
    else:
        return False


while True:
    t.sleep(60)
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()
    sat_longitude = float(data["iss_position"]["longitude"])
    sat_latitude = float(data["iss_position"]["latitude"])
    position = (sat_longitude, sat_latitude)
    print(position)
    response.raise_for_status()

    above_location = check_coordinates(sat_longi=sat_longitude, sat_lati=sat_latitude)
    parameter = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1][0]) + 5
    sunset = int(data["results"]["sunset"].split("T")[1][0]) + 5
    print(sunrise)
    print(sunset)
    time = dt.datetime.now()
    current_time = time.hour
    print(current_time)
    if above_location:
        if current_time >= sunset or current_time <= sunrise:
            my_email = "atest3645@gmail.com"
            password = "poddar@398"
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email,
                                    to_addrs="tpoddar2001@gmail.com",
                                    msg="Subject:INTER-NATIONAL-SPACE-STATION LOCATION\n\nTonmay Look Above In The "
                                        "Sky The ISS is Over There")
