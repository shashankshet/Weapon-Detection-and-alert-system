import os
from twilio.rest import Client




client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='++919876543456',
                        from_='+19548803109'
                    )

print(call.sid)
