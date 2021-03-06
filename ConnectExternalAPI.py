from flask import Flask, request, make_response, jsonify,abort
import json
import os
import linebot

from linebot import (
    LineBotApi, WebhookHandler,WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,ConfirmTemplate,MessageAction,
    QuickReply,QuickReplyButton,MessageEvent,DatetimePickerAction,PostbackAction,PostbackEvent,CarouselTemplate,
	CarouselColumn,ButtonsTemplate,URIAction,DatetimePickerTemplateAction
)
import config
from getAdditionalInfo import *
from getApplicationData import *

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


def updateRichMenu(userid,role):
    if role == 'Students':
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_STUDENT)
    if role == 'LF':
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_LF)
    if role == 'Staffs':
        line_bot_api.link_rich_menu_to_user(userid, config.RICHMENU_ID_STAFF)
    return 'Menu changed'

def getMessageContent(message_id):
     message_content = line_bot_api.get_message_content(message_id)
     return str(message_content)

def pushMgsReqToLF(sub,date,userId,sec,leavetype):
    from getApplicationData import getLFId,getIDFromMatchUser,getName,getLname,getUserId
    lfid = getLFId(sub)
    studentid = getIDFromMatchUser(userId)
    name = getName("Students",studentid)
    lname = getLname("Students",studentid)
    to = getUserId("LF",lfid)
    print(lfid)
    print(to)
    if leavetype == 'Business':
        line_bot_api.push_message(to, TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='นักศึกษา '+str(name)+' '+str(lname)+' '+str(sec)+'\nรหัส: '+str(studentid)+' ขอลากิจ\nวิชา '+str(sub)+'\nวันที่ '+str(date),
            actions=[
                MessageAction(
                    label='อนุมัติ',
                    text='อนุมัติคำขอลา ของนักศึกษารหัส:'+ str(studentid)
                ),
			    MessageAction(
                    label='ไม่อนุมัติ',
                    text='ไม่อนุมัติคำขอลา ของนักศึกษารหัส:' + str(studentid)
                )
            ]
        )
    ))
    else:
        lfid = getLFId(sub)
        studentid = getIDFromMatchUser(userId)
        name = getName("Students",studentid)
        lname = getLname("Students",studentid)
        to = getUserId("LF",lfid)
        print(lfid)
        print(to)
        if leavetype == 'Sick':
            line_bot_api.push_message(to, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='นักศึกษา '+str(name)+' '+str(lname)+' '+str(sec)+'\nรหัส: '+str(studentid)+' ขอลาป่วย\nวิชา '+str(sub)+'\nวันที่ '+str(date),
                actions=[
                    MessageAction(
                        label='อนุมัติ',
                        text='อนุมัติคำขอลา ของนักศึกษารหัส:'+ str(studentid)
                    ),
			        MessageAction(
                        label='ไม่อนุมัติ',
                        text='ไม่อนุมัติคำขอลา ของนักศึกษารหัส:' + str(studentid)
                    )
                ]
            )
        ))
    return 'send success'

def pushMsgQuickReplyStaffId(userId,staffs,name):
    line_bot_api.push_message(userId, TextSendMessage(text='เลือกเจ้าหน้าที่ที่ต้องการส่งค่ะ',
                         quick_reply=QuickReply(items=[
                              QuickReplyButton(action=MessageAction(label=name[0], text='ส่งคำถามให้เจ้าหน้าที่ '+staffs[0])),
                              QuickReplyButton(action=MessageAction(label=name[1], text='ส่งคำถามให้เจ้าหน้าที่ '+staffs[1]))
                           ])))
    return 'send quick reply'

def pushMsgConfirmMissedClass(userId,sub,ID,message):
    from getApplicationData import getName , getLname
    name = getName("Students",ID)
    lname = getLname("Students",ID)
    line_bot_api.push_message(userId, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='แจ้งเตือน นักศึกษา '+str(name)+' '+str(lname)+' '+'\nรหัส: '+str(ID)+' ขาดเรียน\nวิชา '+str(sub)+'\n'+str(message),
                actions=[
                    MessageAction(
                        label='ยืนยัน',
                        text='ยืนยันเเจ้งเตือนการขาดเรียน'
                    ),
			        MessageAction(
                        label='ยกเลิก',
                        text='ยกเลิกการทำรายการ'
                    )
                ]
            )
        ))

def pushMsgConfirmNews(userId,subject,date,content,section,title):
    line_bot_api.push_message(userId, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='หัวข้อ: '+str(title)+'\nวิชา '+str(subject)+'\nวันที่'+str(date)+'\n'+str(content)+'\nแจ้งนักศึกษา '+str(section),
                actions=[
                    MessageAction(
                        label='ยืนยัน',
                        text='ยืนยันเเจ้งเตือนข่าวสาร'
                    ),
			        MessageAction(
                        label='ยกเลิก',
                        text='ยกเลิกการทำรายการ'
                    )
                ]
            )
        ))

def pushQuestionToStaff(answer,question,refno):
    
    line_bot_api.push_message(answer, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='คำถาม: '+str(question),
                actions=[
                    MessageAction(
                        label='ตอบคำถาม',
                        text='ตอบคำถาม refno: '+refno
                    ),
			        MessageAction(
                        label='ส่งต่อ',
                        text='ต้องการส่งคำถาม'+refno+'ไปยังเจ้าหน้าที่คนอื่น'
                    )
                ]
            )
        ))
    return 'success'

def pushConfirmToStaff(ans,userId,refno,question):
    print('pushconfirm'+refno)
    line_bot_api.push_message(userId, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='คำถาม: '+str(question) + '\nคำตอบ: '+str(ans),
                actions=[
                    MessageAction(
                        label='ยืนยัน',
                        text='ยืนยันการตอบคำถาม'
                    ),
			        MessageAction(
                        label='แก้ไข',
                        text='ต้องการแก้ไขคำตอบ'
                    )
                ]
            )
        ))
    return 'sendConfirmAlready'

def pushConfirmCallQuestion(userId,amount):
    line_bot_api.push_message(userId, TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='มีคำถามที่ยังไม่ถูกส่งไปยังเจ้าหน้าที่อยู่ '+str(amount) + ' คำถาม\nคุณต้องการเรียกดูหรือไม่',
                actions=[
                    MessageAction(
                        label='ทั้งหมด',
                        text='ต้องการเรียกดูคำถามทั้งหมด '+str(amount)+' คำถาม' 
                    ),
			        MessageAction(
                        label='กำหนดจำนวน',
                        text='ต้องการเรียกดูแบบกำหนดจำนวน'
                    )
                ]
            )
        ))

def pushMsgLogTrainingFile(req,userId,ID):
    from getAdditionalInfo import getDate
    from getApplicationData import getName , getIDFromMatchUser,getName
    from getApplicationData import getotherstaff
    receiver = []
    receiver=getotherstaff(ID)
    print("pushMsgLogTrainingFile"+str(receiver))
    print(str(len(receiver)))
    for index in range(len(receiver)):
        to=receiver[index]
        print(to)
        nameStaff = getName("Staffs",getIDFromMatchUser(receiver[index]))
        print(nameStaff)
        message = 'เจ้าหน้าที่: '+nameStaff+' ได้ทำการ\nDownload Training File \n วันที่ '+getDate(req)
        pushMessage(to,str(message))
    return 'send success'

