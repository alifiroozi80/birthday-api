import os
import requests
from datetime import datetime
import smtplib
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def send_mail(msg: str) -> None:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(
            user=email,
            password=password
        )
        connection.sendmail(
            from_addr=email,
            to_addrs="alifiroozizamani@gmail.com",
            msg=msg
        )


r = requests.get(url="https://ali-birthday-api.herokuapp.com/all")
status_code = r.status_code

if status_code == 200:
    res = r.json()
    users = res.get("users")

    for user in users:
        d = datetime.now()
        today = d.strftime("%Y-%m-%d")
        date = user.get("birth")

        if today == date:
            send_mail(
                f"Subject: Birthday Alert! \n\n Today is birth of {user.get('name')} "
                f"{user.get('family')}...\n Wish him/her lock!\n{date}"
            )
else:
    send_mail(f"Subject: Status Code {status_code}! \n\n Something naughty is happening on server side...")
