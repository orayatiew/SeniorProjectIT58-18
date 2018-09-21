from flask import Flask, request, make_response, jsonify,abort
import json
import os

import config
from getDataFromDialogflow import *
from getDataFromFirebase import *
from ConnectLineAPI import *
from authentication import *
from announcementLF import *
from LeaveRequest import *
app = Flask(__name__)
log = app.logger

@app.route("/", methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        action = getAction(req) #def from getDataFromDialogflow.py
    except AttributeError:
        return 'json error'

    # Action Switcher
    if action == 'auth.request':
        res = auth_role(req)
    if action == 'auth.confirm':
        res = authentications(req)
    if action == 'input.otp':
        res = checkOTP(req)
    if action =='event.announcementLF':
        res = request_announcementLF(req)
    if action =='cancelclass':
        res = pushMsg_cancelclass(req)
    if action == 'compensatory':
        res = pushMsg_compensatory(req)
    if action == 'score':
        res = pushMsg_score(req)
    if action == 'quiz':
        res = pushMsg_quiz(req)
    if action =='missedClass':
        res = comfirm_MissedClass(req)
    if action =='pushMissClass':
        res = pushMsg_MissClass(req) #here
    if action == 'leavereq':
        res = leaveRequest(req)
    if action == 'pushReqToLf':
        res = pushReqToLf(req)
    if action == 'approve':
        res = approveReq(req)
    if action == 'reject':
        res = rejectReq(req)
    else: 
        log.error('Unexpected action.') 

    print('Action: ' + action) 
    print('Response: ' + res)
    return make_response(jsonify({'fulfillmentText': res}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))
