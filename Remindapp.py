from twilio.rest import Client
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv 


"""First ask what it wants to do"""
# 0 Ask name and email if first time.
# Show menu
# 1 Add appnt
# 2 Show appnt
# 3 Cancel appnt
# 
# Other features like send appointment reminders 1 day before...

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


def applist_send():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)
        for row in json_reader:
            appointments.append(row)

    for appointment in appointments:

        

        body = f'Hello, {appointment['name']}, Your appointment at dental B is on {appointment['appointment_date_str']}'
        send_smsreminder(appointment['phone'], body)

def applist_add():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)
      
def apptlist_del():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)
        