#! /usr/bin/python
# -*- coding: utf-8 -*-
#==========================================================
#Titre: Envvoie du courrier
#
#
#Par: Paco SAMBA
#===========================================================


import smtplib,time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

def SendMail(filename,path,p):

    if p=="porte":

        sender= "your_mail@...."
        passwrd="your_psswd"
        recept = " receiver@..."
        objetMessage="quelqu'un à frapper à ta porte"
        mailServer='smtp.mail.yahoo.fr'
 
        msg = MIMEMultipart()
 
        msg['From'] = sender
        msg['To'] = recept
        msg['Subject'] = objetMessage
 
        body = "quelqu'un  frappe a ta porte"
 
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(str(path),"rb")
 
        part = MIMEBase('application', "octet-stream")
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
        msg.attach(part)
 
        server = smtplib.SMTP(mailServer, 587)
        server.starttls()
        server.login(sender,passwrd)
        text = msg.as_string()
        server.sendmail(sender, recept, text)
        server.quit()

    else:
        d=time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime())
        sender= "cityflame@yahoo.fr"
        passwrd="shimenta"
        recept = "sambapaco@yahoo.fr"
        objetMessage="intru le "+ str(d)
        mailServer='smtp.mail.yahoo.fr'
 
        msg = MIMEMultipart()
 
        msg['From'] = sender
        msg['To'] = recept
        msg['Subject'] = objetMessage
 
        body = "intru chez toi le "+str(d)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(mailServer, 587)
        server.starttls()
        server.login(sender,passwrd)
        text = msg.as_string()
        server.sendmail(sender, recept, text)
        server.quit()
