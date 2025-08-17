from twilio.rest import Client
import os
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv 

# import appointmentlist.csv 

load_dotenv()

today = datetime.now().date()

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
mynum = os.environ.get("mynum")
twilionum = os.environ.get("twilionum")

client = Client(account_sid, auth_token)


def send_smsreminder(to_number, message_body): 
    '''send sms using the twilio API.'''
    message = client.messages.create(
        to = to_number,
        from_= twilionum,
        body= message_body 
    )
    print(f"Message sent to {to_number}")

appointments = []

with open('appointmentlist.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        appointments.append(row)

for appointment in appointments:

    

    body = f'Hello, {appointment['name']}, Your appointment at dental B is on {appointment['appointment_date_str']}'
    send_smsreminder(appointment['phone'], body)