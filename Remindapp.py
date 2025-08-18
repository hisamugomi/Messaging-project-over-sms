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

@app.route("/sms", methods = ['POST'])
def sms_reply():
    message_body = request.values.get('Body', '')
    from_number = request.values.get('From', '')

    print(f"received message from {from_number}: {message_body}")

    if message_body == "Show" :
        applist_send()
    else: print("What going on")


    return "", 200


def applist_add():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)
      
def apptlist_del():
    with open('appointmentlist.json', 'r') as json_file:
        json_reader = json.load(json_file)

def get_ai_response(user_input):
    """Sends a message to AI and returns response."""
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"An error occured: {e}"
    
ai_message = get_ai_response("Hello, How can I buy a tesla?")



# def main_menu():
#     while True:
#         user_input = input("\nHow can I help you today? (Type 'Exit to quit')")
#         if user_input.lower() == 'exit':
#             print('goodbye')
#             break
#         prompt = f"""
# You are a friendly appointment manager chatbot. Your goal is to help the user with their appointments.
# The user's request is: "{user_input}"

# Based on the request, respond in one of the following ways:
# - If the user wants to add an appointment, say "add" and ask for the date and time.
# - If the user wants to see appointments, say "show" and list the upcoming appointments.
# - If the user wants to cancel an appointment, say "cancel" and ask which one to cancel.
# - If the user is asking for a reminder, say "remind" and confirm that you will send a reminder.
# - If the user's request is unclear, respond with a friendly message asking for clarification.
# """
        
#         ai_intent = get_ai_response(prompt).strip().lower()

#         if ai_intent == 'add':
#             print("Okay lets add a new appointment")


# response = MessagingResponse()
# response.message(f"You said: {user_input}")
# return str(response)


if __name__ == "__main__":
    app.run(debug=True)