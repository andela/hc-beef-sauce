from twilio.rest import Client
from django.conf import settings


def send(to, ctx):
    """
    Send sms to a relevant user.
    
    :param to: sms recipient
    :type to: string
    :param ctx: holds affected check as well as all other user checks
    :type ctx: dict
    """
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=ctx["check"].name + " check has gone " + ctx["check"].get_status(),
        from_="+16788317394",
        to = to
    )
