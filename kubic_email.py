#-*- coding:utf-8 -*-
# from __future__ import print_function
# from googleapiclient.discovery import build
# from apiclient import errors
# from httplib2 import Http
# import base64
# from google.oauth2 import service_account

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

loginAddr = "elecindy@handong.ac.kr"
senderAddr='kubic@handong.edu' 
# adminAddr='jhpark@handong.ac.kr' 
# adminAddr = 'kubic@handong.edu'
adminAddr = "elecindy@handong.ac.kr"



# service = service_account_login()

def send_veri_email(email, app_name, app_purpose, key):    
    service = smtplib.SMTP('smtp.gmail.com', 587)
    service.starttls()
    service.login(loginAddr, 'vgjweuwvngkzgmfn')

    msg = MIMEText(\
    '<html><h1>본 활용을 확인하시고 활용 승인 또는 활용 반려 버튼을 클릭해주세요.</h1>'
    '<br>이메일:'+email + \
    '<br>활용명:'+ app_name + \
    '<br>활용목적:' + app_purpose + \
    '<br> <a href="https://kubic.handong.edu:15000/acceptPreUser?key='+key+'">활용 신청 확인</a>'
    "</html>", 'html', _charset='UTF-8')

    msg['Subject'] = '[KUBiC] Open API 승인 요청 from '+ email
    msg['From'] = senderAddr
    msg['To'] = adminAddr
    # try: service.users().messages().send(userId="me", body={'raw': base64.urlsafe_b64encode(msg.as_string())}).execute()
    # except: service.users().messages().send(userId="me", body={'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode('utf8')}).execute()

    service.sendmail(senderAddr, adminAddr, msg.as_string())
    service.quit()

def send_info_email(email, app_name, app_purpose, authKey):
    service = smtplib.SMTP('smtp.gmail.com', 587)
    service.starttls()
    service.login(loginAddr, 'vgjweuwvngkzgmfn')
    
    msg = MIMEText('승인이 완료되었습니다.\n 서비스키를 복사하여 이용하세요.\n활용명:'+app_name+'\n활용목적:'+app_purpose+'\n 서비스키:'+authKey)
    msg['Subject'] = '[KUBiC] Open API 활용이 승인되었습니다.'
    msg['from'] = senderAddr
    msg['to'] = email
    # service.users().messages().send(userId="me", body={'raw': base64.urlsafe_b64encode(msg.as_string())}).execute()
    service.sendmail(senderAddr, email, msg.as_string())
    service.quit()

def send_refuse_email(email, app_name, app_purpose, reason):
    service = smtplib.SMTP('smtp.gmail.com', 587)
    service.starttls()
    service.login(loginAddr, 'vgjweuwvngkzgmfn')
    
    msg = MIMEText('[KUBiC] Open API 활용이 반려되었습니다.\n 반려 사유를 확인 후 재신청해주세요. \n활용명:'+app_name+'\n활용목적:'+app_purpose+'\n 반려사유:'+ reason)
    msg['Subject'] = '[KUBiC] Open API 활용이 반려되었습니다.'
    msg['from'] = senderAddr
    msg['to'] = email
    # service.users().messages().send(userId="me", body=msg).execute()
    service.sendmail(senderAddr, email, msg.as_string())
    service.quit()

# def service_account_login():
#   SCOPES = ['https://www.googleapis.com/auth/gmail.send']
#   SERVICE_ACCOUNT_FILE = 'service-key.json'

#   credentials = service_account.Credentials.from_service_account_file(
#           SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#   delegated_credentials = credentials.with_subject(adminAddr)
#   service = build('gmail', 'v1', credentials=delegated_credentials)
#   return service


# send_veri_email('elecindy@handong.ac.kr','하이','안녕','dd')