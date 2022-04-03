#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText

def send_veri_email(email, app_name, app_purpose):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('elecindy@handong.ac.kr', 'vgjweuwvngkzgmfn')
    msg = MIMEText('내용 : 본문내용 테스트입니다.\n 활용명:'+ app_name + '\n활용목적:' + app_purpose + '\n인증: https://kubic.handong.edu:15000/registerManual?email=' + email + '&app_name=' + app_name + '&app_purpose=' + app_purpose)
    msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'
    s.sendmail("kubic@kubic.handong.edu", "jhpark@handong.ac.kr", msg.as_string())
    # s.sendmail("kubic@kubic.handong.edu", "elecindy@handong.ac.kr", msg.as_string())
    s.quit()

def send_info_email(email, app_name, app_purpose, authKey):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('elecindy@handong.ac.kr', 'vgjweuwvngkzgmfn')
    msg = MIMEText('내용 : 본문내용 테스트입니다.\n활용명:'+app_name+'\n활용목적:'+app_purpose+'\n authKey:'+authKey)
    msg['Subject'] = '제목 : 메일 보내기 테스트입니다.'
    s.sendmail("kubic@kubic.handong.edu", email, msg.as_string())
    s.quit()

# send_veri_email('ehhom10004@naver.com','하이','안녕')