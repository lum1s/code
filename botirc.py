#!/usr/local/bin/python

from lib import *
from data import *
import socket
import ssl
import time
import random
import urllib2
import sqlite3
import itertools

server = set_server()
port = set_port()
channel = set_channel()
thxList = set_thxList()
botnick = set_botnick()
password = set_password()
saysomething = set_saysomething()
something_to_say = set_something_to_say()
operator = set_op1()
text = ""
i=0
fun = 0
ssl0 = 'TRUE'

dataBase = set_dataBase()
log = set_log()
pytania = set_pytania()
sqlCommon = set_sqlCommon()


if 'TRUE' in ssl0:
    irc_C = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    irc = ssl.wrap_socket(irc_C)
else:
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

print "Establishing connection to [%s]" % (server)
# Connect
irc.connect((server,port))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :sms\n")
irc.send("PASS %s\n" % (password))
irc.send("NICK "+ botnick +"\n")

while True:
    time.sleep(0)

    try:
        text2=irc.recv(2040)
        print text2
        text = text2.lower()

        textT = text2.split(":")
        textTT = textT[1].split("!")
        nick = textTT[0]

        if text.find(':!off') !=-1:
               for x in operator:
                   if textTT[0] == x or textTT[1].find(x)!=-1:
                        fun = mode(irc,"sleep",channel)

        if text.find(':!on') !=-1:
                for x in operator:
                   if textTT[0] == x or textTT[1].find(x)!=-1:
                        fun = mode(irc,"activate",channel)

        if text2.find('PRIVMSG luBot :') ==-1:
            if (text2.find(channel) !=-1) and (text2.find("PRIVMSG") !=-1):
                if (':,add?' in text):
                    for x in operator:
                       if textTT[0] == x or textTT[1].find(x)!=-1:
                            addDB(irc,dataBase,text)

                text3 = cleanDialog(irc,channel,text2)
                if (' :!' in text) or (' :,' in text):
                    print "Cmd found, skipped."
                else:
                    print "Zapamietano %s" %text3
                    f2 = open(log,'a')
                    f2.write("%s\n" %text3)
                    f2.close()

            # Prevent Timeout
            if text2.find('PING') != -1:
                irc.send('PONG ' + text.split() [1] + '\r\n')

            if text.find('change your nick') !=-1:
                identify(irc,password)
                time.sleep(4)
                join_channel(irc,channel)
            else:
                if text.find('is not registered') !=-1 or text.find('nie jest zarejestrowany') !=-1:
                    join_channel(irc,channel)
                else:
                    join_channel(irc,channel)

            if text2.find('VERSION') !=-1 or text2.find('MODE') !=-1:
                 join_channel(irc,channel)

            if fun == 1:
                if text.find(':saysomething') !=-1:
                    say(irc,text,channel)
                if text.find(':!swim') !=-1:
                    swim(irc,channel)
                if text.find(':!dance') !=-1:
                    dance(irc,channel)
                if text.find(':!cofee') !=-1:
                    cofee(irc,channel)
                if text.find(':!all') !=-1:
                    call_all(irc,channel)
                if text2.find(' JOIN ') !=-1:
                    say_hi(irc,channel,text)
                if text2.find(' PART ') !=-1:
                    say_by(irc,text,channel)
                if text.find(':!bagiety') !=-1:
                    bagiety(irc,channel)
                if text.find(':!clean') !=-1:
                    clean(irc)
                for k in thxList:
                    if k.lower() in text:
                        print 'Slowo %s znalezione w %s' %(k,text)
                        dziekuje(irc,text,channel)
                if (':!db_new' in text):
                    for x in operator:
                        if textTT[0] == x or textTT[1].find(x)!=-1:
                            createDB(irc,dataBase)
                if ':!db_show' in text:
                    showDB(irc,dataBase)
                if ':!db_find' in text:
                    tmp = text.split(':!db_find')
                    searchDB(irc,dataBase,tmp[1].strip())
                if text.find(':!info') !=-1:
                    for x in operator:
                        if textTT[0] == x or textTT[1].find(x)!=-1:
                            irc.send("NOTICE " + nick + " Options:" + "\n")
                            irc.send("NOTICE " + nick + " :  *Siema" + "\n")
                            irc.send("NOTICE " + nick + " :  *saysomething" + "\n")
                            irc.send("NOTICE " + nick + " :  *!off" + "\n")
                            irc.send("NOTICE " + nick + " :  *!on" + "\n")
                            irc.send("NOTICE " + nick + " :  *!all" + "\n")
                            irc.send("NOTICE " + nick + " :  *!clean" + "\n")
                            irc.send("NOTICE " + nick + " :  *!bagiety" + "\n")
                            irc.send("NOTICE " + nick + " :  *Say hi if some one JOIN" + "\n")
                            irc.send("NOTICE " + nick + " :  *Say bye if some one LEAVE" + "\n")
                            irc.send("NOTICE " + nick + " :  *!swim" + "\n")
                            irc.send("NOTICE " + nick + " :  *!dance" + "\n")
                            irc.send("NOTICE " + nick + " :  *!cofee" + "\n")
                watchIRC(irc,channel,dataBase,text,nick)

        else:
            if (':,add?' in text):
                    for x in operator:
                        if textTT[0] == x or textTT[1].find(x)!=-1:
                            addDB(irc,dataBase,text)
            if (':!db_new' in text) and (operator[1] in text):
                createDB(irc,dataBase)
            if (':!db_show' in text) and (operator[1] in text):
                showDB(irc,dataBase)
            if (':!join' in text) and (operator[1] in text):
                ch = text.split('!join')
                print 'ch: %s' %ch[1]
                join_channel(irc,ch[1])
            if (':!db_find' in text) and (operator[1] in text):
                tmp = text.split(':!db_find')
                searchDB(irc,dataBase,tmp[1].strip())
            if text.find(':!info') !=-1:
                    for x in operator:
                        if textTT[0] == x or textTT[1].find(x)!=-1:
                            irc.send("NOTICE " + nick + " : Options:" + "\n")
                            irc.send("NOTICE " + nick + " :  *Siema" + "\n")
                            irc.send("NOTICE " + nick + " :  *saysomething" + "\n")
                            irc.send("NOTICE " + nick + " :  *!off" + "\n")
                            irc.send("NOTICE " + nick + " :  *!on" + "\n")
                            irc.send("NOTICE " + nick + " :  *!all" + "\n")
                            irc.send("NOTICE " + nick + " :  *!clean" + "\n")
                            irc.send("NOTICE " + nick + " :  *!bagiety" + "\n")
                            irc.send("NOTICE " + nick + " :  *Say hi if some one JOIN" + "\n")
                            irc.send("NOTICE " + nick + " :  *Say bye if some one LEAVE" + "\n")
                            irc.send("NOTICE " + nick + " :  *!swim" + "\n")
                            irc.send("NOTICE " + nick + " :  *!dance" + "\n")
                            irc.send("NOTICE " + nick + " :  *!cofee" + "\n")


    except Exception:
        continue
