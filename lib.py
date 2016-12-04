#!/usr/local/bin/python

import socket
import ssl
import time
import random
import urllib2
import sqlite3
import itertools

def get_title(irc,url,channel):
        print 'Url: %s' %url
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        webpage = response.read()
        if '<title>' in str(webpage):
            title = str(webpage).split('<title>')[1].split('</title>')[0]
        if '<Title>' in str(webpage):
            title = str(webpage).split('<Title>')[1].split('</Title>')[0]
        if '<TITLE>' in str(webpage):
            title = str(webpage).split('<TITLE>')[1].split('</TITLE>')[0]
        print title
        irc.send('PRIVMSG ' + channel + ' :Title \002***"' + title + '"***\002' +'\n')

def createDB(irc,dataBase):
        print 'New DB will be created now.'
        conn = sqlite3.connect(dataBase)
        c = conn.cursor()
        c.execute('''CREATE TABLE fortunki
                     (time text, keyphrase text, response text)''')
        #print ("INSERT INTO fortunki VALUES ('00:00:00','test','test')")
        c.execute("INSERT INTO fortunki VALUES ('00:00:00','test','test')")
        conn.commit()
        conn.close()


def searchDB(irc,dataBase,text):
        print 'Searching DB...'
        con = sqlite3.connect(dataBase)
        cur = con.cursor()
        #print ("SELECT response FROM fortunki WHERE keyphrase LIKE '" + text + "'")
        cur.execute("SELECT COUNT(*) FROM fortunki WHERE keyphrase LIKE '" + text + "'")
        i=cur.fetchone()
        #print "i: %s" %str(i).replace('(','').replace(',)','')
        if str(i).replace('(','').replace(',)','')=='0':
            #print "Brak znalezionych"
            text2 = '0'
        else:
            cur.execute("SELECT response FROM fortunki WHERE keyphrase LIKE '" + text + "'")
            hh = []
            i = cur.fetchall()
            something_to_say = random.choice(i)
            text2 = something_to_say
            #print "text2= !%s!" %text2
            #irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", " + text +"\n")
        return text2

def watchIRC(irc,channel,dataBase,text,nick):
        tmp = ' ' + cleanDialog(channel,text) + ' '
        for s in sqlCommon:
            if s in tmp.lower():
                print "SQL statement in line, ommit the line."
                tmp = ''
                break
        if tmp !='':
            if 'http' in text:
                print 'found link to ommit.'
            else:
                print 'DB is verifying IRC text.'
                con = sqlite3.connect(dataBase)
                cur = con.cursor()
                #print ("SELECT keyphrase FROM fortunki WHERE time NOT LIKE ''")
                cur.execute("SELECT keyphrase FROM fortunki WHERE time NOT LIKE ''")
                i = cur.fetchall()
                #print 'i = %s' %i
                #print 'tmp= %s' %tmp
                #dokladne wyszukiwanie frazy
                resp = searchDB(dataBase, tmp.lower().strip())
                #print "resp: %s" %resp
                if resp !='0':
                        print ':%s, %s' %(nick,resp)
                        irc.send("PRIVMSG " + channel + " :" + nick + ", " + str(resp).replace("(u'",'').replace("',)",'') +"\n")
                else:
                    #mniej dokladne wyszukiwanie
                    for ii in i:
                        #print 'ii = %s' %ii
                        jj = (' ' + str(ii).replace("(u'",'').replace("',)",'') + ' ')
                        #print 'jj= %s' %jj
                        if jj.lower() in tmp.lower():
                            #print 'Znalazlem tekst: %s w %s' %(str(ii).replace("(u'",'').replace("',)",''),tmp)
                            resp = searchDB(dataBase, str(ii).replace("(u'",'').replace("',)",''))
                            print ':%s, %s' %(nick,str(resp).replace("(u'",'').replace("',)",''))
                            irc.send("PRIVMSG " + channel + " :" + nick + ", " + str(resp).replace("(u'",'').replace("',)",'') +"\n")
                            break


def showDB(irc,dataBase):
        con = sqlite3.connect(dataBase)
        cur = con.cursor()
        cur.execute('SELECT * FROM fortunki')
        i=0
        while True:
            d = cur.fetchone()
            if d == None:
                break
            print d[0], d[1], d[2]
            i=i+1

def addDB(irc,dataBase,text):
        print 'Passphrase will be added to DB'
        conn = sqlite3.connect(dataBase)
        c = conn.cursor()
        if ',add?' in text:
            tmp= (text.split(',add?'))
            keyphrase = tmp[1].split(',add!')
            print 'Dodaje: %s' %keyphrase[0]
            response = keyphrase[1].strip()
            print 'Dodaje: %s' %response
        print ("INSERT INTO fortunki VALUES ('00:00:00'," + "'" + keyphrase[0].strip() + "'" + "," + "'" + response + "'" + ")")
        c.execute("INSERT INTO fortunki VALUES ('00:00:00'," + "'" + keyphrase[0].strip() + "'" + "," + "'" + response + "'" + ")")
        conn.commit()
        conn.close()

def delDB(irc):
        print 'Passphrase will be deleted from DB.'

def fortunki(irc):
        #http://fortunki.dug.net.pl/
        #<pre><code></code></pre>
        url= 'http://fortunki.dug.net.pl/losowa'
        print 'Url: %s' %url
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        webpage = response.read()
        smieszki = []
        if '<pre><code>' in str(webpage):
            tmp = str(webpage).split('<pre><code>')[1].split('</code></pre>')[0]
            tmp2 = tmp.splitlines()
            print tmp2
            for x in tmp2:
                smieszki.append(((x.replace('&lt;','')).replace('&gt;',':')).replace('&quot;','"'))
        for z in smieszki:
            print z
            irc.send('PRIVMSG ' + channel + ' :' + z + '\n')

def identify(irc,password):
        irc.send("PRIVMSG Bronek :IDENTIFY " + password +"\n")

def join_channel(irc,channel):
        irc.send("JOIN "+ channel +"\n")

def call_all(irc,channel):
        irc.send("NAMES "+ channel +"\n")
        text=irc.recv(2040)
        textT = text.split(":")
        print textT[2]
        irc.send("PRIVMSG " + channel + " :Wolam \002" + textT[2] + "\002" +"\n")


def hello(irc,text,channel):
        if 'PRIVMSG luBot' in text:
            print "Kurwy sie podszywaja."
        else:
            textT = text.split(":")
            textTT = textT[1].split("!")
            irc.send("PRIVMSG " + channel + " :Siema, " + textTT[0] + "!" + "\n")

def say(irc,text,channel):
            with open(log, 'r') as f2: logT=f2.read().splitlines()
            something_to_say = random.choice(logT)
            f2.close
            textT = text.split(":")
            textTT = textT[1].split("!")
            text = something_to_say
            irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", " + text +"\n")

def swim(irc,channel):
        for i in range(0,random.randrange(1,10)):
            time.sleep(2)
            text = "o/"
            irc.send("PRIVMSG " + channel + " :" + text +"\n")
            time.sleep(2)
            text = "\o"
            irc.send("PRIVMSG " + channel + " :" + text +"\n")

def dance(irc,channel):
        for i in range(0,random.randrange(1,10)):
            time.sleep(2)
            text = "(o("
            irc.send("PRIVMSG " + channel + " :" + text +"\n")
            text = ")o)"
            time.sleep(2)
            irc.send("PRIVMSG " + channel + " :" + text +"\n")

def say_hi(irc,channel,text):
        textT = text.split(":")
        textTT = textT[1].split("!")
        irc.send("PRIVMSG " + channel + " :Witaj " + textTT[0] + ' na '+ channel + "!\n")
        irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", pamietaj o panujacych tu zasadach:)" + "\n")

def say_bye(irc,text,channel):
        textT = text.split(":")
        textTT = textT[1].split("!")
        irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", zegnaj towarzyszu!\n")

def cofee(irc,channel):
        cup = "      )" + "\n" + "      (" + "\n" + "      )"+ "\n" + " __.--(--." + "\n" +  "|| |     | " + "\n" + "  \\|     | " + "\n" +  "   \.    ."+ "\n" +  "    `---'" + "\n"
        cupIrc = ["      )", "      (", "      )", " __.--(--.",  "|| |     | ", "  \\|     | ",  "   \.    .",  "    `---'"]
        for l in cupIrc:
            irc.send("PRIVMSG " + channel + " :" + l +"\n")

def bagiety(irc,channel):
        irc.send("NAMES "+ channel +"\n")
        text=irc.recv(2040)
        textT = text.split(":")
        print textT[2]
        textTT = textT[2].split(' ')
        lista2 = ""
        for l in textTT:
            if '@' in l:
                lista2 = lista2 + l + ", "
                print 'Bagieta: %s\n' %lista2

        irc.send("PRIVMSG " + channel + " :Bagiety juz jado! \002" + lista2 + "\002" +"\n")

def clean(irc):
        f2 = open(log,'w')
        f2.close()

def lol(irc,text,channel):
        textT = text.split(":")
        textTT = textT[1].split("!")
        print ":To bylo malo smieszne"
        irc.send("PRIVMSG " + channel + " :To bylo malo smieszne " + textTT[0] + " :/" + '\n')
        #irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", check this out!" + '\n')

def dziekuje(irc,text,channel):
        textT = text.split(":")
        textTT = textT[1].split("!")
        print "Sciagaj majtki %s" %textTT[0]
        irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", sciagaj majtki :)" +'\n')

def lapa(irc,text,channel):
        textT = text.split(":")
        textTT = textT[1].split("!")
        print "o/ %s" %textTT[0]
        irc.send("PRIVMSG " + channel + " :" + textTT[0] + ", o/" +'\n')

def cleanDialog(irc,channel,text):
        irc.send("NAMES "+ channel +"\n")
        textL=irc.recv(2040)
        textT = textL.split(":")
        textTT = textT[2].split(' ')
        #print 'Lista userow %s\n' %textT[2]
        if 'http' in text:
            if 'privmsg' in text:
                print 'did du nafin'
            else:
                print "Wykrylem link %s" %text
                textT2 = text.split("http")
                text2 = 'http' + str(textT2[1])
                print "Zapisalem link %s" %(text2)
                get_title(text2)
                return text2
        else:
            text = text.lower()
            textT2 = text.split(":")
            #print "Text wypowiedziany %s" %textT2[2]
            for ll in textTT:
                #print 'Szukanie %s' %ll
                if ll in textT2[2]:
                    #print 'Znalazlem "%s" w "%s", teraz wyczyszcze.\n' %(ll,textT2[2])
                    text2 = textT2[2].replace(ll,'')
                    text2 = text2.replace(',','')
                    text2 = text2.replace(':','')
                    #print '"%s" usuniety, nowy "%s"\n' %(ll,text2)
                    if '?' in textT2[2]:
                        f = open(pytania,'a')
                        f.writelines(textT2[2] + '\n')
                        f.close()
                    return text2
            return textT2[2]

def mode(irc,string,channel):
        if string == "sleep":
            fun = 0
            print ("Fun set off: %d" %fun)
            irc.send("PRIVMSG " + channel + " :Off..." +"\n")
        if string == "activate":
            fun = 1
            print ("Fun set on: %d" %fun)
            irc.send("PRIVMSG " + channel + " :On..." +"\n")
        return fun

