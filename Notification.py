import os
from twilio.rest import Client
from dotenv import load_dotenv

class sendMessages:

    def __init__(self):
        load_dotenv(os.path.join(os.getcwd(), 'twilio.env'))

        self.accountSID = os.environ.get('TWILIO_ACCOUNT_SID')
        self.authToken = os.environ.get('TWILIO_AUTH_TOKEN')
        self.phone = os.environ.get('TWILIO_PHONE')

        self.client = Client(self.accountSID, self.authToken)
        self.recipientNumber = '+447871596495'

    def sendMessage(self):
        message = self.client.messages.create(
            body="Program execution finished",
            from_=self.phone,
            to=self.recipientNumber
        )
        print(message.sid)

