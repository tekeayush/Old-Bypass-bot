from os import environ
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import time
import re
import requests
import urllib.parse
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qs
from base64 import b64decode
from urllib.parse import unquote
from lxml import etree
import hashlib
import json
import base64
import logging
from modules.appdrive import appdrive_dl
from modules.rocklink import rocklinks_bypass
logging.basicConfig(level=logging.INFO)

for log_name, log_obj in logging.Logger.manager.loggerDict.items():
     if log_name != 'pyrogram':
          log_obj.disabled = True

LOGGER = logging.getLogger(__name__)

API_ID = ''
API_HASH =''
BOT_TOKEN = ''


bot = Client('shorturlbypasserbot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)

@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    LOGGER.info(f"{message.chat.first_name} Just Started me")
    await message.reply(
        f'''**Hi {message.chat.first_name}!**\n'''
        '''I'm Short Link Bypasser Bot.\n
        <b>Send Me Shorten Url And I Will Give You Direct Link</b>
        
        <b>╭──「⭕️ **Supported Sites** ⭕️」</b>
        <b>├ 1) gplink.in</b>
        <b>├ 2️) shorte.st</b>
        <b>├ 3️) ouo.io</b> ( Unstable )
        <b>├ 4️) droplink.co</b>
        <b>├ 5️) gofile.io</b>
        <b>├ 6️) linkvertise.com</b>
        <b>├ 7️) bit.ly</b>
        <b>├ 8️) adf.ly</b>
        <b>├ 9️) wetransfer.com</b>
        <b>├ 10) rekonise.com</b>
        <b>├ 11) Rocklink</b>
        
        Note :- In development stage.
       ''')



@bot.on_message(filters.regex(r'\bhttps?://.*gplink\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    LOGGER.info(f"reciverd new link from {message.from_user.id} {message.chat.first_name} Bypassing {url}")
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = await gplinks(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
#      await message.reply(
#        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
#        reply_markup=reply_markup
#      )
     await message.reply(f'{bypassed}')
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'{e}', quote=True)
#_________________________________________________________________________________
#ROCKLINK BYPASS
@bot.on_message(filters.regex(r'\bhttps?://.*rocklink\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    LOGGER.info(f"reciverd new link from {message.from_user.id} {message.chat.first_name} Bypassing {url}")
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = rocklinks_bypass(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True)
#_________________________________________________________________________________

#APPDRIVE
@bot.on_message(filters.regex(r'\bhttps?://.*appdrive\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    LOGGER.info(f"reciverd new link from {message.from_user.id} {message.chat.first_name} Bypassing {url}")
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = appdrive_dl(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'its a test bot so Appdrive is only available on @bypasss_bot', quote=True)                
#GDTOT        
@bot.on_message(filters.regex(r'\bhttps?://.*gdtot\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    LOGGER.info(f"reciverd new link from {message.from_user.id} {message.chat.first_name} Bypassing {url}")
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = await gdtot_dl(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'its a test bot so Gdtot is only available on @bypasss_bot', quote=True)
# add your crypt cookie here
crypt = "" 

# ==========================================

def parse_info(res):
    title = re.findall(">(.*?)<\/h5>", res.text)[0]
    info = re.findall('<td\salign="right">(.*?)<\/td>', res.text)
    parsed_info = {
        'error': True,
        'message': 'Link Invalid.',
        'title': title,
        'size': info[0],
        'date': info[1]
    }
    return parsed_info

# ==========================================

async def gdtot_dl(url):
    client = requests.Session()
    client.cookies.update({ 'crypt': crypt })
    res = client.get(url)

    info = parse_info(res)
    info['src_url'] = url

    res = client.get(f"https://new.gdtot.top/dld?id={url.split('/')[-1]}")
    
    try:
        url = re.findall('URL=(.*?)"', res.text)[0]
    except:
        info['message'] = 'The requested URL could not be retrieved.',
        return info

    params = parse_qs(urlparse(url).query)
    
    if 'msgx' in params:
        info['message'] = params['msgx'][0]
    
    if 'gd' not in params or not params['gd'] or params['gd'][0] == 'false':
        return info
    
    try:
        decoded_id = base64.b64decode(str(params['gd'][0])).decode('utf-8')
        gdrive_url = f'https://drive.google.com/open?id={decoded_id}'
        info['message'] = 'Success.'
    except:
        info['error'] = True
        return info

    info['gdrive_link'] = gdrive_url
    bypassed = info['gdrive_link']
    
    return bypassed
    
# ==========================================       
        
#GDTOT_CLOSED

@bot.on_message(filters.regex(r'\bhttps?://.*destyy\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    LOGGER.info(f"reciverd new link from {message.from_user.id} {message.chat.first_name} Bypassing {url}")
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = await sh_st_bypass(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

@bot.on_message(filters.regex(r'\bhttps?://.*ouo\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = await ouo_bypass(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 


@bot.on_message(filters.regex(r'\bhttps?://.*droplink\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)
    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = await droplink(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

@bot.on_message(filters.regex(r'\bhttps?://.*gofile\S+') & filters.private)
async def link_handler(bot, message):
    url = message.matches[0].group(0)

    try:
     await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
     bypassed = await gofile_dl(url)
     BUTTONS = [
       [
         InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
         InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
       ]
     ]
     reply_markup=InlineKeyboardMarkup(BUTTONS)
     await message.reply(
       (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
       reply_markup=reply_markup
     )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 


 #linkvertise
@bot.on_message(filters.regex(r'\bhttps?://.*link\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await lv_bypass(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 


#Bit_ly
@bot.on_message(filters.regex(r'\bhttps?://.*bit.ly\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await bit_ly(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

#bit_ly         
async def bit_ly(url):
  payload = {
    "url": url,
  }

  r = requests.post("https://api.bypass.vip/", data=payload)
  data = r.json()
  return data["destination"]


#rekonise.com
@bot.on_message(filters.regex(r'\bhttps?://.*rekonise.com\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await rekonise(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

#rekonise.com         
async def rekonise(url):
  payload = {
    "url": url,
  }

  r = requests.post("https://api.bypass.vip/", data=payload)
  data = r.json()
  return data["destination"]

#adfly
@bot.on_message(filters.regex(r'\bhttps?://.*barsoocm\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await adfly_bypass(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 
#adfly_public-domain-1
@bot.on_message(filters.regex(r'\bhttps?://.*j.gs\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await adfly_bypass(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

#adfly_public-domain-2
@bot.on_message(filters.regex(r'\bhttps?://.*q.gs\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await adfly_bypass(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 


#wetransfer
@bot.on_message(filters.regex(r'\bhttps?://.*we.tl\S+') & filters.private)
async def link_handler(bot, message):
     url = message.matches[0].group(0)
     try:
      await message.reply(f'ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙʏᴘᴀssɪɴɢ ʏᴏᴜʀ Uʀʟ')   
      bypassed = await wetransfer(url)
      BUTTONS = [
        [
          InlineKeyboardButton('💀 ᴏʀɪɢɪɴᴀʟ Uʀʟ 💀', url = url),
          InlineKeyboardButton('🔥 ʙʏᴘᴀssᴇᴅ ᴜʀʟ 🔥', url = bypassed)
        ]
      ]
      reply_markup=InlineKeyboardMarkup(BUTTONS)
      await message.reply(
        (f'❤️{message.chat.first_name} ʏᴏᴜʀ ʟɪɴᴋ ʜᴀs ʙᴇᴇɴ ʙʏᴘᴀssᴇᴅ \n\n 👇 ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇\n\n 🔥 ʙʏᴘᴀssᴇᴅ ʙʏ <b>@bypasss_bot</b>'),
        reply_markup=reply_markup
      )
     except Exception as e:
         LOGGER.error(e)
         await message.reply(f'Eɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀ ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ɪᴛ ᴛᴏ ᴏᴡɴᴇʀs', quote=True) 

# wetransfer
WETRANSFER_API_URL = "https://wetransfer.com/api/v4/transfers"
WETRANSFER_DOWNLOAD_URL = WETRANSFER_API_URL + "/{transfer_id}/download"

        


def _prepare_session() -> requests.Session:
    """Prepare a wetransfer.com session.
    Return a requests session that will always pass the required headers
    and with cookies properly populated that can be used for wetransfer
    requests.
    """
    s = requests.Session()
    r = s.get("https://wetransfer.com/")
    m = re.search('name="csrf-token" content="([^"]+)"', r.text)
    s.headers.update(
        {
            "x-csrf-token": m.group(1),
            "x-requested-with": "XMLHttpRequest",
        }
    )

    return s


def wetransfer(url):
    """Given a wetransfer.com download URL download return the downloadable URL.
    The URL should be of the form `https://we.tl/' or
    `https://wetransfer.com/downloads/'. If it is a short URL (i.e. `we.tl')
    the redirect is followed in order to retrieve the corresponding
    `wetransfer.com/downloads/' URL.
    The following type of URLs are supported:
     - `https://we.tl/<short_url_id>`:
        received via link upload, via email to the sender and printed by
        `upload` action
     - `https://wetransfer.com/<transfer_id>/<security_hash>`:
        directly not shared in any ways but the short URLs actually redirect to
        them
     - `https://wetransfer.com/<transfer_id>/<recipient_id>/<security_hash>`:
        received via email by recipients when the files are shared via email
        upload
    Return the download URL (AKA `direct_link') as a str or None if the URL
    could not be parsed.
    """
    # Follow the redirect if we have a short URL
    if url.startswith("https://we.tl/"):
        r = requests.head(url, allow_redirects=True)
        url = r.url

    recipient_id = None
    params = urllib.parse.urlparse(url).path.split("/")[2:]

    if len(params) == 2:
        transfer_id, security_hash = params
    elif len(params) == 3:
        transfer_id, recipient_id, security_hash = params
    else:
        return None

    j = {
        "intent": "entire_transfer",
        "security_hash": security_hash,
    }
    if recipient_id:
        j["recipient_id"] = recipient_id
    s = _prepare_session()
    r = s.post(WETRANSFER_DOWNLOAD_URL.format(transfer_id=transfer_id), json=j)

    j = r.json()
    if "direct_link" in j:
        return j["direct_link"]
    else:
        xo = f"The content is expired/deleted."
        return xo

def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b

    key = list(a + b)
    i = 0

    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j                   
                    break
        i+=1
    
    key = ''.join(key)
    decrypted = b64decode(key)[16:-16]

    return decrypted.decode('utf-8')

# ==========================================

def adfly_bypass(url):
    res = requests.get(url).text
    
    out = {'error': False, 'src_url': url}
    
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
        
    url =decrypt_url(ysmm)

    if re.search(r'go\.php\?u\=', url):
        url = b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    out['bypassed_url'] = url
    link=url
    return link

async def lv_bypass(url):
      headers = {
"Host": "bypass.bot.nu",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
"Accept": "*/*",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Referer": "bypass.bot.nu/",
"Connection": "keep-alive",
                }
      data = requests.get(f"https://bypass.bot.nu/bypass2?url={url}", headers=headers)
      link = data.json()["destination"]
      return link        
async def gofile_dl(url):
    api_uri = 'https://api.gofile.io'
    password = 'xcyber@2'
    client = requests.Session()
    res = client.get(api_uri+'/createAccount').json()
    
    data = {
        'contentId': url.split('/')[-1],
        'token': res['data']['token'],
        'websiteToken': 'websiteToken',
        'cache': 'true',
        'password': hashlib.sha256(password.encode('utf-8')).hexdigest()
    }
    res = client.get(api_uri+'/getContent', params=data).json()
    links = []
    contents = res["data"]["contents"]
   
    for content in contents.values():
            link = content["link"]
            if link not in links:
                links.append(link)

    return content["link"]
  
async def droplink(url):
        client = requests.Session()
        res = client.get(url)
        ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]
        h = {"referer": ref}
        res = client.get(url, headers=h)
        bs4 = BeautifulSoup(res.content, "lxml")
        inputs = bs4.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs}
        h = {
            "content-type": "application/x-www-form-urlencoded",
            "x-requested-with": "XMLHttpRequest",
        }
        p = urlparse(url)
        final_url = f"{p.scheme}://{p.netloc}/links/go"
        time.sleep(3.1)
        res = client.post(final_url, data=data, headers=h).json()
        return res["url"]


def RecaptchaV3(ANCHOR_URL):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer

ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr'

# -------------------------------------------
# OUO BYPASS

async def ouo_bypass(url):
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):

        if res.headers.get('Location'):
            break

        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        
        ans = RecaptchaV3(ANCHOR_URL)
        data['x-token'] = ans
        
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return res.headers.get('Location')
    


async def sh_st_bypass(url):    
    client = requests.Session()
    client.headers.update({'referer': url})
    p = urlparse(url)
    
    res = client.get(url)

    sess_id = re.findall('''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', res.text)[0]
    
    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': sess_id,
        'callback': '_'
    }
    time.sleep(5) # !important
    
    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace('\/','/')
    
    return dest_url

async def gplinks(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f"{p.scheme}://{p.netloc}/links/go"
    res = client.head(url)
    header_loc = res.headers["location"]
    param = header_loc.split("postid=")[-1]
    req_url = f"{p.scheme}://{p.netloc}/{param}"
    p = urlparse(header_loc)
    ref_url = f"{p.scheme}://{p.netloc}/"
    h = {"referer": ref_url}
    res = client.get(req_url, headers=h, allow_redirects=False)
    bs4 = BeautifulSoup(res.content, "html.parser")
    inputs = bs4.find_all("input")
    time.sleep(10) # !important
    data = { input.get("name"): input.get("value") for input in inputs }
    h = {
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "XMLHttpRequest"
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()["url"].replace("/","/")
    except: 
        return "Could not Bypass your URL :("

# ==============================================
LOGGER.info('I AM ALIVE')
bot.run()
