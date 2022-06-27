from aiohttp import request
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Defaults, Updater, Dispatcher, CallbackContext, MessageHandler, Filters
import gdshortener
from instagramy import InstagramUser
from urllib import response
import json
import requests
import imgbbpy
import qrcode
import os, time, random

BOT_TOKEN = "5196000920:AAECLxm23glDzqVUXVhbJkkwyzuH-jzTHIU"

def whoisLookup(update, context):
    if len(context.args) > 0:
        domain = context.args[0].lower()
        whoIs = requests.get(f"https://api.ip2whois.com/v2?key=E9S1CSDLISDZBYD2D8IDE95FKYOXKAJV&domain={domain}").text
        whoIs = json.loads(whoIs)

        response =  f"<b>┏━━━━━━━━━━━━━━━</b>\n"
        response += f"<b>📊 Validator By LillyFish</b>\n"
        response += f"<b>┗━━━━━━━━━━━━━━━</b>\n\n"
        response += f"<b>┠⌬Domain: </b><pre>{whoIs['domain']}</pre>\n"
        response += f"<b>┠⌬Created: </b><pre>{whoIs['create_date'][:10]}</pre>\n"
        if len(whoIs['expire_date']) > 2:
            response += f"<b>┠⌬Expire: </b><pre>{whoIs['expire_date'][:10]}</pre>\n"
        if len(whoIs['update_date']) > 2:
            response += f"<b>┠⌬Updated: </b><pre>{whoIs['update_date'][:10]}</pre>\n"
        response += f"<b>┠⌬Domain Age: </b><pre>{round((whoIs['domain_age']/365),2)} Years</pre>\n"
        response += f"<b>┠⌬Register: </b><pre>{whoIs['registrar']['name']}</pre>\n"
        response += f"<b>┠⌬Nameserver: </b><pre>{whoIs['nameservers'][0]}</pre>\n"

        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)



updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("whois", whoisLookup))
updater.start_polling()
updater.idle()