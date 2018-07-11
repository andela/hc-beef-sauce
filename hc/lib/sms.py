from twilio.rest import Client
from django.conf import settings
from djmail.template_mail import InlineCSSTemplateMail

def send(to, ctx):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=ctx["check"].name + " check has gone " + ctx["check"].get_status(),
        from_="+16788317394",
        to = to
    )
