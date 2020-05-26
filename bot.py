#Importing Modules
import discord
import pandas as pd

#Defining the bot as 'client'
client = discord.Client()

#Prints key information for setting up the bot
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    server_name = client.get_guild(<discord-server-id>)
    print(client.guilds)
    print(server_name)
    print(client.emojis)

#Waits for keyword, posts message based on user's text and creates reactions on message for sign ups
@client.event
async def on_message(message):
    sign_up_channel = client.get_channel(<signupchannel-id>)
    bot_channel = client.get_channel(<botchannel-id>)

    if message.channel == bot_channel:
        if message.content.find('!event') != -1:
            msg = message.content[6:]
            await sign_up_channel.send(f'**New Event!** {msg}')

    if message.channel == sign_up_channel:
        if message.content.find('**New Event!**') != -1:
            await message.add_reaction(client.get_emoji(<emoji-tank-id>)) #tank
            await message.add_reaction(client.get_emoji(<emoji-heal-id>)) #heal
            await message.add_reaction(client.get_emoji(<emoji-dd-id>)) #dd
            await message.add_reaction(client.get_emoji(<emoji-decline-id>)) #decline

#Creates sign ups when users respond with reactions
@client.event
async def on_raw_reaction_add(payload):
    #getting a user clicking a reaction
    msg_user = client.get_user(payload.user_id)

    #check not bot
    if client.user == msg_user:
        return
    #getting the original message
    orig_msg = await client.http.get_message(<signupchannel-id>, payload.message_id)

    #putting original mesage to data frame
    df = pd.DataFrame(list(orig_msg.items()))
    content_msg = df.iat[2,1]
    msg = (str(msg_user) + '-' + str(payload.emoji))

    #removing all previous sign ups on decline
    if str(payload.emoji) == '<:<emoji-decline-name>:<emoji-decline-id>>':
        tank = (str(msg_user) + '-' + str(client.get_emoji(<emoji-tank-id>)))
        heal = (str(msg_user) + '-' + str(client.get_emoji(<emoji-heal-id>)))
        dd = (str(msg_user) + '-' + str(client.get_emoji(<emoji-dd-id>)))

        full_msg = str(content_msg)
        for r in ((tank, ''), (dd, ''), (heal, '')):
            full_msg = full_msg.replace(*r)
        full_msg = full_msg +'\n  '+ msg
    else:
        refuse = (str(msg_user) + '-' + str(client.get_emoji(<emoji-decline-id>)))
        full_msg = content_msg.replace(refuse, '')+'\n '+ msg

    #changing the original message
    await client.http.edit_message(<signupchannel-id>, payload.message_id, content=full_msg)

#Removes sign ups when users removes reactions
@client.event
async def on_raw_reaction_remove(payload):
    msg_user = client.get_user(payload.user_id)

    #checking not bot
    if client.user == client.get_user(payload.user_id):
        return

    orig_msg = await client.http.get_message(<signupchannel-id>, payload.message_id)
    msg = (str(msg_user) + '-' + str(payload.emoji))

    df = pd.DataFrame(list(orig_msg.items()))
    content_msg = df.iat[2,1]

    roll_back_msg = str(content_msg).replace(msg, '')
    await client.http.edit_message(<signupchannel-id>, payload.message_id, content=roll_back_msg)

client.run(<your_bot_token>)