# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACd79f39ac30b9742e43c153ea68a04918'
auth_token = '40520b503bb15b03ab4e71093eb084b3'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+19044743219',
                     to='+6587188040'
                 )

print(message.sid)