from aiohttp import request
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Defaults, Updater, Dispatcher, CallbackContext, MessageHandler, Filters
import gdshortener
from instagramy import InstagramUser
from urllib import response
import json
import requests
import os
import qrcode


url = "https://youtube-mp3-download1.p.rapidapi.com/dl"
querystring = {"id": "do7psVA1K3g"}
headers = {
    "X-RapidAPI-Host": "youtube-mp3-download1.p.rapidapi.com",
    "X-RapidAPI-Key": "0d5a53bf68msh8068e5fbc3fc0c7p1703aajsn01682edf5cf2"
}
audioResult = requests.request("GET", url, headers=headers, params=querystring).text
audioResult = json.loads(audioResult)
# ytAudio = audioResult["link"]

print(audioResult)