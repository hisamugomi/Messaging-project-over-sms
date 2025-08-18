from twilio.rest import Client
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv 
import google.generativeai as genai
from flask import Flask, request

"""First ask what it wants to do"""
# 0 Ask name and email if first time.
# Show menu
# 1 Add appnt
#   - 
# 2 Show appnt
# 3 Cancel appnt
# 
# Other features like send appointment reminders 1 day before...

app = Flask(__name__)

@app.route('/')
def hello_World():
    return('Hello World')
    

load_dotenv()
aiapi_key = os.environ.get("google-ai-studio-api-key")
genai.configure(api_key = aiapi_key )
model = genai.GenerativeModel('gemini-1.5-flash')

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
    appointments = []
    try:
        with open('appointmentlist.json', 'r') as json_file:
            json_reader = json.load(json_file)
            print(json_reader)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    for row in json_reader:
            appointments.append(row)

    for appointment in appointments:
        body = f"Hello, {appointment['name']}, Your appointment at dental B is on {appointment['appointments']}"
        send_smsreminder(appointment['phone'], body)




def applist_add():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)
      
def apptlist_del():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)

def get_ai_intent(user_input):
    prompt = f"""
    You are a friendly appointment manager chatbot. Your goal is to help the user with their appointments.
    The user's request is: "{user_input}"
    
    Based on the request, respond with only one of the following words: "add", "show", "cancel", "remind", or "other".
    """
    return get_ai_response(prompt).strip().lower()


@app.route("/sms", methods = ['POST'])
def sms_reply():
    message_body = request.values.get('Body', '')
    from_number = request.values.get('From', '')

    print(f"received message from {from_number}: {message_body}")

    ai_intent = get_ai_intent(message_body)

    if message_body == "Show" :
        applist_send()
    else: print("What going on")
    return "", 200

main_menu()

if __name__ == "__main__":
    app.run(debug=True)