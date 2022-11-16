from load_save_bougs import save_bougs


class BougMessage:
    def __init__(self, id, author, content, tipers):
        self.id = id
        self.author = author
        self.content = content
        self.tipers = tipers


def reaction_update(bot, reaction, user):
    message = reaction.message

    if message.id in bot.dict_msg.keys():
        boug_msg = bot.dict_msg[message.id]
    else:
        boug_msg = BougMessage(message.id, message.author, message.content, [])
        bot.dict_msg[message.id] = boug_msg

    if isinstance(reaction.emoji, str):
        emoji_name = reaction.emoji
    else:
        emoji_name = reaction.emoji.name

    print(
        f"{user} reacted with {emoji_name} on '{message.content}' written by {message.author}"
    )

    if message.author == user:
        print(f"{user} a réagi à son propre message (aka auto-suceur move)")
    elif emoji_name == "🪙":
        if user in boug_msg.tipers:
            print(f"{user} already tipped this msg")
        else:
            boug_msg.tipers.append(user)
            # add a timestamp to the dict_tip_ts of the boug
            print(
                f"{user} tipped {bot.dict_boug[int(message.author.id)].dict_tip_ts.get(user.id)}")
            if (bot.dict_boug[int(message.author.id)].dict_tip_ts.get(user.id) is None):
                bot.dict_boug[int(message.author.id)
                              ].dict_tip_ts[user.id] = message.created_at
                print(
                    f"IT'S TIP TIME !! {message.author} gagne +1BGC grâce au tip de {user}")
                give_money(bot, source=user, target=message.author, amount=1)
            else:
                max_period = 10
                print(
                    f"last tip: {bot.dict_boug[int(message.author.id)].dict_tip_ts[user.id]}")
                if ((message.created_at - bot.dict_boug[int(message.author.id)].dict_tip_ts[user.id]).seconds < max_period):
                    print(
                        f"{user} already tipped this boug in the last {max_period} seconds")
                    return
                else:
                    bot.dict_boug[int(message.author.id)
                                  ].dict_tip_ts[user.id] = message.created_at
                    print(
                        f"IT'S TIP TIME !! {message.author} gagne +1BGC grâce au tip de {user}"
                    )
                    give_money(bot, source=user,
                               target=message.author, amount=1)
    else:
        print(f"{user} paye {message.author} en visibilité")


def give_money(bot, source, target, amount):
    # Target & Author
    id_target = int(target.id)
    id_author = int(source.id)
    target_boug = bot.dict_boug[id_target]
    author_boug = bot.dict_boug[id_author]
    # amount = min(amount, author_boug.money)

    # Transaction
    target_boug.money += amount
    # author_boug.money -= amount # uncomment pour que la réaction coûte
    save_bougs(bot)
