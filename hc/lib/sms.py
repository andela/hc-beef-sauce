from twilio.rest import Client
from django.conf import settings
from djmail.template_mail import InlineCSSTemplateMail

def send(name, to, ctx):
    account_sid = "AC56cf28b96824e51e4d8db731da509d47"
    auth_token = "3326c5cfb017273a273dd77b605c7208"
    client = Client(account_sid, auth_token)

    o = InlineCSSTemplateMail(name)
    ctx["SITE_ROOT"] = settings.SITE_ROOT
    o.send(to, ctx)

    message = client.messages.create(
        body=o,
        from_="+16788317394",
        to = to
    )

def alert(to, ctx):
    send("alert", to, ctx)