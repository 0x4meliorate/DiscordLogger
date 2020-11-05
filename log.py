import discord
from discord import File
import json
import os
import time
import datetime
import requests

client = discord.Client()
token = "TOKEN-HERE"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.guild == None:
        if message.author != client.user:
            if len(message.attachments) > 0:
                media = str(message.attachments[0].url)
                extension = media.split(".")
                img_data = requests.get(media).content
                with open("media/" + str(message.id) + "." + str(extension[-1]), "wb") as handler:
                    handler.write(img_data)

            return

@client.event
async def on_message_delete(message):
    if message.guild == None:
        if message.author != client.user:
            embedVar = discord.Embed(title="Logged:", description="", color=0x272727)
            author = client.get_user(message.author.id)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            embedVar.add_field(name="Author", value=str(author), inline=False)
            embedVar.add_field(name="Action", value="Deleted at "+st, inline=False)
            if message.content != "":
                embedVar.add_field(name="Message", value=message.content, inline=False)

            embedVar.add_field(name="Timestamp", value=message.created_at, inline=False)
            await message.channel.send(embed=embedVar)
            if len(message.attachments) > 0:
                for file in os.listdir("media/"):
                    if file.startswith(str(message.id)):
                        await message.channel.send(file=File("media/"+file))
                        os.remove("media/"+file)
            return

@client.event
async def on_message_edit(before, after):
    if after.author != client.user or before.author != client.user:
        if after.guild == None or before.guild == None:
            embedVar = discord.Embed(title="Logged:", description="", color=0x272727)
            author = client.get_user(after.author.id)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            embedVar.add_field(name="Author", value=str(author), inline=False)
            embedVar.add_field(name="Action", value="Edited at "+st, inline=False)
            embedVar.add_field(name="Message", value=before.content, inline=False)
            embedVar.add_field(name="Timestamp", value=before.created_at, inline=False)
            await after.channel.send(embed=embedVar)
            return


client.run(token, bot=False)
