import os
from twilio.rest import Client


account_sid = 'ACa99143e3debeaf62a7fa341c1e819f47'
auth_token = 'e377b2d41a4261106a0cac837314df50'

client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+919986428818',
                        from_='+19548803109'
                    )

print(call.sid)