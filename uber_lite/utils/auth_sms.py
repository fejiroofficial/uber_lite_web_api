import os
from os.path import dirname, join
from twilio.rest import Client
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

phone_number = os.getenv('TWILIO_PHONE_NUMBER')


def send_sms(telephone_number, message_body):
    client.messages \
        .create(
            body=message_body,
            from_=phone_number,
            to=telephone_number
        )
