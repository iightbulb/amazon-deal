import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

URL = "https://www.amazon.com/Goose-Down-Ultralight-Mummy-Backpacking-Sleeping-Bag-0-15-30-Degree/dp/B06XRLQ3SB/ref=sr_1_5?crid=1JHR045VFID6O&keywords=down+sleeping+bag&qid=1669621408&sprefix=down+sleeping+bag%2Caps%2C284&sr=8-5"


def configure():
    load_dotenv()


def send_email(cost):
    with smtplib.SMTP("smtp.gmail.com") as connection:  # URL OF EMAIL SERVER
        connection.starttls()
        connection.login(os.getenv('my_email'), os.getenv('my_password'))
        subject = "Hello!"
        text = f"Your bag currently costs ${cost}.\nHere's the link: {URL}"
        message = "Subject: {}\n\n{}".format(subject, text)
        connection.sendmail(os.getenv('my_email'), os.getenv('my_email'), message)


configure()

headers = {
    "Accept-Language": "en-ZA",
    "User-Agent": "Chrome/107.0.0.0",
}
response = requests.get(url=URL, headers=headers)
contents = response.text

soup = BeautifulSoup(contents, "lxml")
cost = soup.find(name="span", class_="a-offscreen")
raw_cost = float(cost.getText().split("$")[1])
print(raw_cost)

if raw_cost < 220:
    send_email(raw_cost)
