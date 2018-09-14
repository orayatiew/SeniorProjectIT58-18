from flask import Flask, request, make_response, jsonify,abort
import json
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import config
from getDataFromDialogflow import *
app = Flask(__name__)
log = app.logger

line_bot_api = config.LINEBOTAPI_ACCESSTOKEN
handler = config.LINEBOTAPI_SECRETTOKEN

def pushMessage(to,message):

    line_bot_api.push_message(to, TextSendMessage(text = message))
    return 'send success'

def pushmultiMessage(to,message):
    line_bot_api.multicast(to, TextSendMessage(text = message))
    return 'send success'

def pushImageMessage(to,link):
    line_bot_api.multicast(to, ImageSendMessage(original_content_url=link, preview_image_url=link))
    return 'send success'

def updateRichMenu(userid,role):
    if role == 'Students':
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_STUDENT)
    else:
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_STAFF_LF)
    return 'Menu changed'

def getMessageContent(message_id):
     message_content = line_bot_api.get_message_content(message_id)
     return str(message_content)