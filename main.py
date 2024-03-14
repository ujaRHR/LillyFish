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

s = gdshortener.ISGDShortener()

apiKey = 'YOUR_TELEGRAM_BOT_TOKEY_KEY'

# Credit Variable for Re-use
credit = f"<b>┏━━━━━━━━━━━━━━━</b>\n<b>🙋🏻‍♂️ Bot By @amoux_sh</b>\n<b>┗━━━━━━━━━━━━━━━</b>\n"

# Start Command
def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bonjour <i>{update.message.from_user.first_name}</i> 👋 \nI am LillyFish, a cute link shortner. \nCheck more by typing /help...")

# Link Shortener
def shortner(update, context):
    if len(context.args) == 1:
        try:
            mainLink = context.args[0]
            randomShortener = s.shorten(f"{mainLink}")
            qrCode = f'\'https://chart.apis.google.com/chart?cht=qr&chs=150x150&choe=UTF-8&chld=H|0&chl={randomShortener[0]}\''

            response = f"<b>┏━━━━━━━━━━━━━━━━━</b>\n"
            response +=f"<b>┠ ✅ S U C C E S S ✅</b>\n\n"

            response +=f"<b>┠⌬ Your shortened URL is:</b>\n"
            response +=f"<b>┠⌬</b> <pre>{randomShortener[0]}</pre>\n"
            response +=f"<b>┠⌬ QR Code:</b> <a href={qrCode}>Here</a>\n\n"

            response += credit
            
            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
        except gdshortener.GDGenericError:
            response = "⚠️ Please enter a valid URL to shorten."
            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
    elif len(context.args) == 2:
        mainLink = context.args[0]
        customName = context.args[1]
        
        try:
            customShortener = s.shorten(url=mainLink, custom_url=customName)
            qrCode = f'\'https://chart.apis.google.com/chart?cht=qr&chs=150x150&choe=UTF-8&chld=H|0&chl={customShortener[0]}\''

            response = f"<b>┏━━━━━━━━━━━━━━━━━</b>\n"
            response +=f"<b>┠ ✅ S U C C E S S ✅</b>\n\n"
            
            response +=f"<b>┠⌬ Your shortened URL is:</b>\n"
            response +=f"<b>┠⌬</b> <pre>{customShortener[0]}</pre>\n"
            response +=f"<b>┠⌬ QR Code:</b> <a href={qrCode}>Here</a>\n\n"

            response += credit

            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
        except gdshortener.GDGenericError:
            response = f"<b>┏━━━━━━━━━━━━━━━━━</b>\n"
            response +=f"<b>┠ ❌ F A I L E D ❌</b>\n\n"
            response +=f"<b>💔 The shortened URL you picked already exists, please choose another.</b>\n\n"
            response +=f"<b>🙋🏻‍♂️ Bot By @dchklg</b>\n"
            response +=f"<b>┗━━━━━━━━━━━━━━━━━</b>"

            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
    else:
        response = "<b>⚠️ Wrong Command Format ⚠️</b>\n\n"
        response += "Example:\n<pre>/short example.com\nor, \n/short example.com myshort10</pre>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Instagram Tools
def instaFinder(update, context):
    try:
        username = context.args[0]
        if "@" in username:
            username = username[1:]

        try:
            preview = "<pre>🔍 Collecting user info...</pre>\n"
            context.bot.sendMessage(chat_id=update.message.chat_id, text=preview)
            session_id = "YOUR_SESSION_ID"
            user = InstagramUser(username, sessionid=session_id)


            response =  "<b>┏━━━━━━━━━━━━━━━</b>\n"
            response += "<b>📊 InstaStats By LillyFish</b>\n"
            response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

            response +=f"<b>🌀 User:</b> <a href='https://instagram.com/{user.username}'>@{user.username}</a>\n"

            if len(user.fullname) > 0:
                response +=f"<b>🥑 Fullname:</b> <pre>{user.fullname}</pre>\n"

            if user.other_info["is_private"]==False:
                if user.other_info["is_private"]==False and user.other_info["is_business_account"]==True:
                    response +=f"<b>⚙️ Type:</b> <pre>Public/Business</pre>\n"
                else:
                    response +=f"<b>⚙️ Type:</b> <pre>Public/Personal</pre>\n"
            if user.other_info["is_private"] == True:
                response +=f"<b>⚙️ Type:</b> <pre>Private</pre>\n"
            
            response +=f"<b>👤 Followers:</b> <pre>{user.number_of_followers}</pre>\n"
            response +=f"<b>👥 Following:</b> <pre>{user.number_of_followings}</pre>\n"
            response +=f"<b>🔰 Total Post:</b> <pre>{user.number_of_posts}</pre>\n"
            response +=f"<b>❇️ Highlighted Reel:</b> <pre>{user.other_info['highlight_reel_count']}</pre>\n"
            if user.is_verified == True:
                response +=f"<b>✅ Verified:</b> <pre>Yes</pre>\n"
            if user.is_verified == False:
                response +=f"<b>✅ Verified:</b> <pre>No</pre>\n"
            if user.website != None:
                response +=f'<b>🌐 Website:</b> <a href="{user.website}">Click Here</a>\n'
            if len(user.biography) > 0:
                response +=f"<b>🗯 Bio:</b> <pre>{user.biography}</pre>\n\n"

            response += credit

            context.bot.sendPhoto(chat_id=update.message.chat_id, photo=user.user_data["profile_pic_url_hd"])
            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
            context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=(update.message.message_id)+1)
        except:
            response = "❌ <b>Username doesn't exist.</b> ❌\n\n<pre>The link you followed may be broken, or the page may have been removed.</pre>"

            response += "\n\n<b>🙋🏻‍♂️ Bot By @dchklg</b>"
            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
            context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=(update.message.message_id)+1)

        os.system("rm -r .instagramy_cache")
    except IndexError:
        response = "<b>⚠️ Wrong Command Format ⚠️</b>\n\n"
        response += "Example: <pre>/insta fifaworldcup</pre>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# IP Address Check
def checkIP(update, context):
    if len(context.args) > 0:
        ip = context.args[0]
        ip = str(ip)
        geoLocation = requests.get(f"http://ipinfo.io/{ip}/geo").text
        geoLocation = json.loads(geoLocation)
        try:
            response =  "<b>┏━━━━━━━━━━━━━━━━━\n</b>"
            response += "<b>┠ ✅ IPTracker by LillyFish ✅</b>\n"
            response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

            response += f"<b>┠⌬ IP:</b> <pre>{geoLocation['ip']}</pre>\n"
            response += f"<b>┠⌬ ISP:</b> <pre>{geoLocation['org'][8:]}</pre>\n"
            response += f"<b>┠⌬ Geolocation:</b> <pre>{geoLocation['loc']}</pre>\n"
            response += f"<b>┠⌬ City:</b> <pre>{geoLocation['city']}</pre>\n"
            response += f"<b>┠⌬ Region:</b> <pre>{geoLocation['region']}</pre>\n"
            response += f"<b>┠⌬ Country:</b> <pre>{geoLocation['country']}</pre>\n"
            response += f"<b>┠⌬ Zip Code:</b> <pre>{geoLocation['postal']}</pre>\n"
            response += f"<b>┠⌬ Timezone:</b> <pre>{geoLocation['timezone']}</pre>\n\n"

            response += credit

            context.bot.sendMessage(chat_id=update.message.chat_id, text=response)
        except:
            response =  "┏━━━━━━━━━━━━━━━━━\n"
            response += "<b>┠ ⚠️ IPTracker by LillyFish ⚠️</b>\n\n"
            response += "<pre>Wrong IP | Please provide a valid ip address.</pre>\n\n"
            response += credit

            context.bot.sendMessage(chat_id=update.message.chat_id, text=response)
    else:
        response = "<b>⚠️ Wrong Command Format ⚠️</b>\n\n"
        response += "Example: <pre>/ip 100.153.0.6</pre>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Random user generator
def randomUser(update, context):
    random = requests.get("https://randomuser.me/api/").text
    random = json.loads(random)
    user = random["results"][0]

    response =  "<b>┏━━━━━━━━━━━━━━━━━</b>\n"
    response += "<b>┠ ✅ Randomizer by LillyFish ✅</b>\n"
    response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

    response += f"<b>┠⌬ Name:</b> <pre>{user['name']['first']} {user['name']['last']}</pre>\n"
    response += f"<b>┠⌬ Gender:</b> <pre>{user['gender']}</pre>\n"
    response += f"<b>┠⌬ Email:</b> <pre>{user['email']}</pre>\n"
    response += f"<b>┠⌬ Phone:</b> <pre>{user['phone']}</pre>\n"
    photo = user["picture"]["large"]
    response +=  "<b>┠⌬ Photo:</b> " + f'<a href="{photo}">View</a>\n'
    address = user['location']
    fullAddress = f"{address['street']['number']} {address['street']['name']}, {address['city']}, {address['state']}, {address['country']}-{address['postcode']}"
    response += f"<b>┠⌬ Address:</b> <pre>{fullAddress}</pre>\n\n"

    response += credit

    context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)

# Upload Image Online
def imgUpload(update, context):
    try:
        context.bot.sendMessage(chat_id=update.message.chat_id, text="<pre>Collecting the data...</pre>")
        client = imgbbpy.SyncClient("!!!YOUR_TOKEN_HERE!!!")
        def rainbow():
            context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+1)
            preview = "<pre>Uploading the image...🟥</pre>"
            context.bot.sendMessage(chat_id=update.message.chat_id, text=preview)
            time.sleep(1)
            preview = "<pre>Uploading the image..🟥 🟧</pre>"
            context.bot.editMessageText(chat_id=update.message.chat_id, message_id=update.message.message_id+2, text=preview)
            time.sleep(1)
            preview = "<pre>Uploading the image.🟥 🟧 🟨</pre>"
            context.bot.editMessageText(chat_id=update.message.chat_id, message_id=update.message.message_id+2, text=preview)
            time.sleep(1)
            preview = "<pre>Uploading the image 🟥 🟧 🟨 🟩</pre>"
            context.bot.editMessageText(chat_id=update.message.chat_id, message_id=update.message.message_id+2, text=preview)
            time.sleep(1)
            context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+2)
        
        file = context.bot.get_file(update.message.document)
        PATH = os.path.basename(file.download())
        allowedExtensions = ["jpg", "png", "gif", "jpeg", "pdf", "bmp", "WEBP"]
        if PATH.endswith(".png") or PATH.endswith(".jpg") or PATH.endswith(".jpeg") or PATH.endswith(".gif") or PATH.endswith(".pdf") or PATH.endswith(".bmp") or PATH.endswith(".webp"):
            image = client.upload(file=PATH)
            rainbow()
            os.system("rm -r " + PATH)

            response =  "<b>┏━━━━━━━━━━━━━━━</b>\n"
            response += "<b>📸 ImgLoader By LillyFish</b>\n"
            response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"
            response += "<b>✅ Uploaded Successfully</b>\n\n"
            imageLink = image.url
            response += f'<b>🌐 Link: </b><a href="{imageLink}">Click Here</a>\n'
            response += f"<b>📊 Size: </b><pre>{round((image.size/1024),2)} KB</pre>\n"
            response += f"<b>🔰 Type: </b><pre>{(image.mime).upper()}</pre>\n\n"    
            response += credit

            context.bot.sendMessage(chat_id=update.message.chat_id, text=response, disable_web_page_preview=True)
        else:
            context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+1)
            response = "⚠️ <b>Filetype is not supported.</b>\n\n"
            response += "Supported Formats: <pre>jpg, png, gif, jpeg, pdf, bmp and webp</pre>"
            context.bot.sendMessage(chat_id=update.message.chat_id, text=response)
            os.system("rm -r " + PATH)
    except:
        context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+1)
        response = "<b>⚠️ Something went wrong. Please specify a valid command.\n\nCheck /help for reference.</b>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Password Generator
def passGenerator(update, context):
    response =  "<b>✅ Random Password ✅</b>\n\n"
    char = "=mh2X3-jpDLG$s#ulKO.9rvMzW*kAP+ZbU@dCI&YgS6/N8Hte_1oRfFw5BaiJ7!xVT4Eqcny%?Q0"
    password = ""
    for x in range(16):
        password += random.choice(char)
    response += f"<b>🔑</b> <pre>{password}</pre>\n\n"
    
    response += f"<b>🙋🏻‍♂ Generated By @dchklg</b>"

    context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Text to QR Code Generator
def text2QrCode(update, context):
    if len(context.args) > 0:
        userArgs = context.args[0:] # ["sahjf", "hhasfas", "sahjhasfa"]
        userText = ' '.join(map(str, userArgs))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=3
        )
        qr.add_data(userText)
        img = qr.make_image()
        img.save("Text_2_QR.png")

        context.bot.sendPhoto(chat_id=update.message.chat_id,  photo=open("Text_2_QR.png", 'rb'), caption='<b>✅ Text to QR Code\n🙋🏻‍♂ Generated By <a href="https://t.me/lillyfish_bot">LillyFish</a></b>', parse_mode="html")
        os.system("rm -r Text_2_QR.png")
    else:
        response = "<b>⚠️ Wrong Command Format ⚠️</b>\n\n"
        response += "Example: <pre>/qr Your Text Here</pre>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# WhoIs Domain Details Check
def whoisLookup(update, context):
    if len(context.args) > 0:
        domain = context.args[0]
        whoIs = requests.get(f"https://api.ip2whois.com/v2?key=[YOUR_TOKEN_HERE]&domain={domain}").text
        whoIs = json.loads(whoIs)

        response =  "<b>┏━━━━━━━━━━━━━━━</b>\n"
        response += "<b>📊 Whois By LillyFish</b>\n"
        response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"
        response += f"<b>┠⌬Domain: </b><pre>{whoIs['domain']}</pre>\n"
        response += f"<b>┠⌬Created: </b><pre>{whoIs['create_date'][:10]}</pre>\n"
        if len(whoIs['expire_date']) > 2:
            response += f"<b>┠⌬Expire: </b><pre>{whoIs['expire_date'][:10]}</pre>\n"
        if len(whoIs['update_date']) > 2:
            response += f"<b>┠⌬Updated: </b><pre>{whoIs['update_date'][:10]}</pre>\n"
        response += f"<b>┠⌬Domain Age: </b><pre>{round((whoIs['domain_age']/365),2)} Years</pre>\n"
        response += f"<b>┠⌬Register: </b><pre>{whoIs['registrar']['name']}</pre>\n"
        response += f"<b>┠⌬Nameserver: </b><pre>{whoIs['nameservers'][0]}</pre>\n\n"
        response += credit

        context.bot.sendMessage(chat_id=update.message.chat_id, text=response, parse_mode="html")
    else:
        response = "<b>⚠️ Wrong Command Format ⚠️</b>\n\n"
        response += "Example: <pre>/whois wikileaks.org</pre>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Email Validator
def emailValidator(update, context):
    if len(context.args) > 0:
        email = context.args[0].lower()
        validOrNot = requests.get(f"https://emailverification.whoisxmlapi.com/api/v2?apiKey=[YOUR_TOKEN_HERE]&emailAddress={email}").text
        validOrNot = json.loads(validOrNot)

        response =  "<b>┏━━━━━━━━━━━━━━━</b>\n"
        response += "<b>🔎 Validator By LillyFish</b>\n"
        response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

        try:
            if 'formatCheck' in validOrNot and 'smtpCheck' in validOrNot and 'dnsCheck' in validOrNot:
                if validOrNot['formatCheck'] == "true" and validOrNot['smtpCheck'] == "true" and validOrNot['dnsCheck'] == "true":
                    response += f"<b>⚙️ Email is Valid</b>\n\n"
        except KeyError:
            response += "";
 
        if validOrNot['dnsCheck'] == "false":
            response += f"<b>❌ Email is invalid ❌</b>\n\n"

        response += f"<b>📩 Email: </b><pre>{validOrNot['emailAddress']}</pre>\n"
        
        if validOrNot['formatCheck'] == "true":
            response += f"<b>✅ Format: </b><pre>Valid</pre>\n"
        if validOrNot['formatCheck'] == "false":
            response += f"<b>❌ Format: </b><pre>Invalid</pre>\n"
        if 'smtpCheck' in validOrNot and validOrNot['smtpCheck'] == "true":
            response += f"<b>🔑 SMTP: </b><pre>Valid</pre>\n"
        if 'smtpCheck' in validOrNot and validOrNot['smtpCheck'] == "false":
            response += f"<b>🔑 SMTP: </b><pre>Invalid</pre>\n"
        if validOrNot['dnsCheck'] == "true":
            response += f"<b>✅ DNS: </b><pre>Valid</pre>\n"
        if validOrNot['dnsCheck'] == "false":
            response += f"<b>❌ DNS: </b><pre>Invalid</pre>\n"
        if validOrNot['disposableCheck'] == "false":
            response += f"<b>🕵️‍♀️ Disposable: </b><pre>No</pre>\n\n"
        if validOrNot['disposableCheck'] == "true":
            response += f"<b>🕵️‍♀️ Disposable: </b><pre>Yes, Temporary Email</pre>\n\n"
        response += credit

        context.bot.sendMessage(chat_id=update.message.chat_id, text=response, parse_mode="html")
    else:
        response = "<b>⚠️ Wrong Command Format ⚠️</b>\n\n"
        response += "Example: <pre>/valid contact@wikileaks.org</pre>"
        context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Activity Suggestions
def activitySuggestion(update, context):
    work = requests.get("https://www.boredapi.com/api/activity/").text
    work = json.loads(work)

    response =  "<b>┏━━━━━━━━━━━━━━━━━</b>\n"
    response += "<b>┠ ✅ Activitia by LillyFish ✅</b>\n"
    response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

    response += f"<b>┠⌬ Activity:</b> <pre>{work['activity']}</pre>\n"
    response += f"<b>┠⌬ Type:</b> <pre>{work['type']}</pre>\n"
    response += f"<b>┠⌬ Participants:</b> <pre>{work['participants']}</pre>\n\n"

    response += credit

    context.bot.sendMessage(chat_id=update.message.chat_id, text=response)

# Tell me a Joke
def tellMeAJoke(update, context):
    joke = requests.get("https://v2.jokeapi.dev/joke/Any?").text
    joke = json.loads(joke)

    response =  "<b>┏━━━━━━━━━━━━━━━━━</b>\n"
    response += "<b>┠ ✅ StolenJokes by LillyFish ✅</b>\n"
    response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

    if "joke" in joke:
        response += f"<b>😐 </b> <pre>{joke['joke']}</pre>\n\n"
        response += credit
    else:
        response += f"<b>⚙️ </b> <pre>{joke['setup']}</pre>\n"
        response += f"<b>😐 </b> <pre>{joke['delivery']}</pre>\n\n"
        response += credit
    
    context.bot.sendMessage(chat_id=update.message.chat_id, text=response)


# Tiktok Downloader
def tiktokDownloader(update, context):
    userLink = context.args[0]
    preview = "<pre>🔍 Processing...</pre>\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=preview)

    url = "https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/vid/index"
    querystring = {"url":userLink}
    headers = {
	    "X-RapidAPI-Host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com",
	    "X-RapidAPI-Key": "[YOUR_TOKEN_HERE]"
    }
    result = requests.request("GET", url, headers=headers, params=querystring).text
    result = json.loads(result)
    
    videoLink = f'{result["video"][0]}.mp4'
    musicLink = f'{result["music"][0]}'

    response = "<b>┏━━━━━━━━━━━━━━━</b>\n"
    response += "<b>📊 Download Completed</b>\n"
    response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"

    response += f'🎬 <a href="{videoLink}">Download Video</a>\n'
    response += f'🎧 <a href="{musicLink}">Download Music</a>\n\n'
    response += f'<pre>a video preview is being sent to you...</pre>'

    context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+1)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.HTML)

# Youtube Downloader
def YTDownloader(update, context):
    userLink = context.args[0]
    videoID = userLink[-11:]
    preview = "<pre>🔍 Processing...</pre>\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=preview)

    # Youtube Audio Downloader
    url = "https://youtube-mp3-download1.p.rapidapi.com/dl"
    querystring = {"id":videoID}
    headers = {
        "X-RapidAPI-Host": "youtube-mp3-download1.p.rapidapi.com",
        "X-RapidAPI-Key": "[YOUR_TOKEN_HERE]"
    }
    audioResult = requests.request("GET", url, headers=headers, params=querystring).text
    audioResult = json.loads(audioResult)
    try:
        ytAudio = audioResult["link"]

        response =  "<b>┏━━━━━━━━━━━━━━━</b>\n"
        response += "<b>📊 YTSmasher By LillyFish</b>\n"
        response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"
        
        if audioResult['status'] == 'fail':
            response += "<b>❌ Conversion Failed </b>\n\n"
            response += f'Link is invalid.\n'
            response += f'<pre>Please try again with correct format...</pre>\n\n'
        else:
            response += "<b>✅ Conversion Completed </b>\n\n"
            response += f'🎧 <a href="{ytAudio}">Download Music</a>\n'
            response += f'<pre>click the link to start downloading...</pre>\n\n'

        response += credit
 
        context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+1)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    except KeyError:
        response = "<b>❌ Something went wrong... Try another -_- </b>\n\n"
        context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=update.message.message_id+1)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Help Menu
def helpMenu(update, context):
    response =  "<b>┏━━━━━━━━━━━━━━━</b>\n"
    response += "<b>⚙️ Help Menu</b>\n"
    response += "<b>┗━━━━━━━━━━━━━━━</b>\n\n"
    response += "<b>/yt url</b> -- <pre>Youtube to MP3</pre>\n"
    response += "<b>/tiktok url</b> -- <pre>Tiktok Downloader</pre>\n"
    response += "<b>/short url</b> -- <pre>Link Shortener</pre>\n"
    response += "<b>/insta username</b> -- <pre>Instagram Stats</pre>\n"
    response += "<b>/ip address</b> -- <pre>IP Address Check</pre>\n"
    response += "<b>/qr text</b> -- <pre>Text to QR Code</pre>\n"
    response += "<b>/whois domain</b> -- <pre>Whois Lookup</pre>\n"
    response += "<b>/valid email</b> -- <pre>Email Validator</pre>\n"
    response += "<b>/random</b> -- <pre>Random User Generator</pre>\n"
    response += "<b>/pass</b> -- <pre>Generate Strong Password</pre>\n"
    response += "<b>/bored</b> -- <pre>Activity Suggestions</pre>\n"
    response += "<b>/joke</b> -- <pre>Tell me a Joke</pre>\n"

    response += "<b>/help</b> -- <pre>Check Help Menu</pre>\n\n"
    response += "<pre>*** Send an uncompressed image to upload it online</pre>\n\n"
    response += credit

    context.bot.sendMessage(chat_id=update.message.chat_id, text=response)


def main() -> None:
    updater = Updater(token=apiKey,defaults=Defaults(parse_mode=ParseMode.HTML))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', startCommand))
    dispatcher.add_handler(CommandHandler('short', shortner))
    dispatcher.add_handler(CommandHandler('insta', instaFinder))
    dispatcher.add_handler(CommandHandler('ip', checkIP))
    dispatcher.add_handler(CommandHandler('random', randomUser))
    dispatcher.add_handler(CommandHandler('bored', activitySuggestion))
    dispatcher.add_handler(CommandHandler('joke', tellMeAJoke))
    dispatcher.add_handler(CommandHandler('help', helpMenu))
    dispatcher.add_handler(CommandHandler('pass', passGenerator))
    dispatcher.add_handler(CommandHandler('qr', text2QrCode))
    dispatcher.add_handler(CommandHandler('whois', whoisLookup))
    dispatcher.add_handler(CommandHandler('valid', emailValidator))
    dispatcher.add_handler(CommandHandler('tiktok', tiktokDownloader))
    dispatcher.add_handler(CommandHandler('yt', YTDownloader))


    dispatcher.add_handler(MessageHandler(Filters._Photo , imgUpload))


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
