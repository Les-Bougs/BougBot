import datetime
from load_save_bougs import save_bougs

def voice_update(bot, member, before, after):
    ts = datetime.datetime.now()
    if before.channel == after.channel:
        print('Voice state changed, but no connection/disconnection')
    else:
        if after.channel and after.channel.name in ('Général', 'les_devs'):
            print(f'{member} connected on {after.channel.name} at {ts}\n')
            bot.dict_boug[member.id].last_connected = ts.strftime("%Y-%m-%d %H:%M:%S")
            save_bougs(bot.dict_boug)
        if before.channel and before.channel.name in ('Général', 'les_devs'):
            print(f'{member} disconnected from {before.channel.name} at {ts}')
            # print(f"{member} has {self.dict_boug[member.id].money} bougcoin")
            member_last_connection = bot.dict_boug[member.id].last_connected
            member_last_connection= datetime.datetime.strptime(member_last_connection, "%Y-%m-%d %H:%M:%S")
            delta = ts - member_last_connection
            print(f'Time spent on {before.channel.name}: {delta.seconds} sec')

            money_gain = delta.seconds
            bot.dict_boug[member.id].money = bot.dict_boug[member.id].money + money_gain
            bot.dict_boug[member.id].last_connected = ts.strftime("%Y-%m-%d %H:%M:%S")
            save_bougs(bot.dict_boug)