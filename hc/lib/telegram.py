import telepot

def send(to, ctx):
    bot = telepot.Bot('604698832:AAFdeZS_dxDcohxIOgRg0hvimV1E6y_MVP8')
    updates = bot.getUpdates()
    for update in updates:
        if 'username' in update["message"]["from"].keys():
            if update["message"]["from"]["username"] == to:
                bot.sendMessage(update["message"]["chat"]["id"], ctx["check"].name + " check has gone " + ctx["check"].get_status())
        else:
            pass
