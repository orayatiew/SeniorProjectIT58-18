﻿from flask import Flask, request, make_response, jsonify,abort
import json
import os

import config
from getDataFromDialogflow import *
from getDataFromFirebase import *
from ConnectLineAPI import *
from collections import OrderedDict

app = Flask(__name__)
log = app.logger

def staffCanceledClass(req):
    year = getParamOutputcontext(req,"years",0)
    date = getParamOutputcontext(req,"date",0)
    date = str(date).replace("T12:00:00+00:00","")
    if year == 'Freshy':
        message = 'ประกาศงดการเรียนการสอนทุกวิชา\nสำหรับนักศึกษาชั้นปี1\nวันที่ '+str(date)
        to = getstudentFreshy()
        pushmultiMessage(to,message)
    if year == 'Sophomore':
        message = 'ประกาศงดการเรียนการสอนทุกวิชา\nสำหรับนักศึกษาชั้นปี2\nวันที่ '+str(date)
        to = getstudentSophomore()
        pushmultiMessage(to,message)
    if year == 'Junior':
        message = 'ประกาศงดการเรียนการสอนทุกวิชา\nสำหรับนักศึกษาชั้นปี3\nวันที่ '+str(date)
        to = getstudentJunior()
        pushmultiMessage(to,message)
    if year == 'Senior':
        message = 'ประกาศงดการเรียนการสอนทุกวิชา\nสำหรับนักศึกษาชั้นปี4\nวันที่ '+str(date)
        to = getstudentSenior()
        pushmultiMessage(to,message)
    if year == 'allyear':
        message = 'ประกาศงดการเรียนการสอนทุกวิชา\nสำหรับนักศึกษาทุกชั้นปี\nวันที่ '+str(date)
        Freshy = getstudentFreshy()
        pushmultiMessage(Freshy,message)
        Sophomore = getstudentSophomore()
        pushmultiMessage(Sophomore,message)
        Junior = getstudentJunior()
        pushmultiMessage(Junior,message)
        Senior = getstudentSenior()
        pushmultiMessage(Senior,message)

    return 'ส่งประกาศไปยังนักศึกษาเรียบร้อยแล้วค่ะ'

def staffExamschedule(req):
    year = getParamOutputcontext(req,"years",0)
    message = 'ประกาศ!!ตารางสอบประกาศแล้ว \nสามารถดูได้ที่เว็บคณะ  https://www.sit.kmutt.ac.th/'
    if year == 'Freshy':
        to = getstudentFreshy()
        pushmultiMessage(to,message)
    if year == 'Sophomore':
        to = getstudentSophomore()
        pushmultiMessage(to,message)
    if year == 'Junior':
        to = getstudentJunior()
        pushmultiMessage(to,message)
    if year == 'Senior':
        to = getstudentSenior()
        pushmultiMessage(to,message)
    if year == 'allyear':
        Freshy = getstudentFreshy()
        pushmultiMessage(Freshy,message)
        Sophomore = getstudentSophomore()
        pushmultiMessage(Sophomore,message)
        Junior = getstudentJunior()
        pushmultiMessage(Junior,message)
        Senior = getstudentSenior()
        pushmultiMessage(Senior,message)

    return 'ส่งประกาศไปยังนักศึกษาเรียบร้อยแล้วค่ะ'