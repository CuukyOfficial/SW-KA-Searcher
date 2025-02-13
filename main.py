import asyncio
import datetime

import discord

from website_check import check_website

# Get token from file
with open("token.txt", "r") as file:
    TOKEN = file.read()

# ID of the target Discord channel
with open("channel_id.txt", "r") as file:
    channel_id = int(file.read())


def last_update_formatted():
    return "Letztes Update: " + datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')


# Discord-Bot
class MyBotClient(discord.Client):
    async def on_ready(self):
        print('Eingeloggt als', self.user)
        channel = self.get_channel(channel_id)

        # Last Update Message ID
        last_update = None

        while True:
            # Überprüfen der Website und Rückgabewert erhalten
            result = check_website()
            if result[0] is False and last_update is not None:
                await last_update.edit(content=last_update_formatted())
            elif result[0] is True:
                await channel.send(content=result[1], file=discord.File(result[2]))

            if last_update is None or result[0] is True:
                last_update = await channel.send(content=last_update_formatted())

            # 15 Minuten warten
            await asyncio.sleep(60 * 15)


# Discord-Bot starten
client = MyBotClient(intents=discord.Intents.default())
client.run(TOKEN)
