#Fly Rod Crosby: Making Cryptoparties Easier since 1897!
#All original material Copyright (C) 2013 Peter Bourgelais
#Original file from xpi2folders: xpi2folders.py Copyright (C) 2011-2012, Kirill Kozlovskiy
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#See the GNU General Public License for more details.
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
import os
import requests
import re
import hashlib
from shutil import copyfile
from bs4 import BeautifulSoup
from urlparse import urlparse
from frc_winconfig import *
from xpi2folders import *
from _winreg import *

import wx

def FRCAlert(text):
     print text
#    if os.path.isfile('log.dat'):
#        f = open('log.dat','a')
#    else:
#        f = open('log.dat','w')
#    f.write(text)
#    f.close()

#Intevation doesn't have an HTTPS download of the file 
#that doesn't throw a certificate error.  Could somebody yell at them, please?	
#Anyway 
def getGPG(url):
    gpg_page=requests.get(url)
    gpg4win_soup = BeautifulSoup(gpg_page.content)
    gpg4win_link=gpg4win_soup.find_all('a', attrs={'href': re.compile('gpg4win-vanilla.*exe$')})[0]['href']
    gpg4win_checksums=gpg4win_soup.find_all('code')
    gpg4win_file=requests.get(gpg4win_link,stream=True) 
    with open('gpg4win.exe','wb') as f:
        for chunk in gpg4win_file.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
	f.close()
    FRCAlert("Calculating and verifying SHA1, which is geek speak for making sure that nobody changed the file during download.\n")
    sha1 = hashlib.sha1()
    f = open('gpg4win.exe','rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    gpg4win_hash = sha1.hexdigest()
    checksum_verified=False
    for checksum in gpg4win_checksums:
        if gpg4win_hash in checksum:
            FRCAlert("SHA1 verified, running installer\n")
            checksum_verified=True
            os.system("gpg4win.exe")
    if checksum_verified == False:
        FRCAlert("SHA1 verification failed!  Hide yo kids!  Hide yo wife!  They messin' with everybody out here!\n")


try:
    import gnupg
    FRCAlert('near gpg init\n')
    gpg=gnupg.GPG()
    FRCAlert('after gpg init\n')
except Exception:
    FRCAlert("GnuPG not found.  Downloading it now.\n")
    FRCAlert("Expect an installer window in 5 minutes.\n")
    getGPG(gpg4win_url)
    import gnupg


#Given an HTTP url, return it with https
def HTTPSthis(url):
    return re.sub(pattern='http', repl='https', string=url)

def printError(text):
    print 'An error occured with your download.  Please show this to your Cruptoparty facilitator: ' + str(text)


#REQUIRE: url and lang are unicode
def getTOR(url, lang):	
    try:
        tor_page=requests.get(url)
        tor_soup = BeautifulSoup(tor_page.content)
        tor_exe_link=''
        tor_sig_link=''
        #If somebody from the Tor Project is reading this, would it kill you to use absolute links?
        FRCAlert('Scraping the Tor Project site for the relevant links\n')
        tor_link_exes=tor_soup.find_all('a', attrs={'href': re.compile('torbrowser-install-.*' + lang + '.*exe$')})
        tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('torbrowser-install-.*' + lang + '\\.exe\\.*asc$')})
        tor_url_parsed=urlparse(url)
        tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc
        
        #print unicode(tor_link_exes) + '\n\n' + unicode(tor_sig_links)
        
        
        for exe_link in tor_link_exes:
            if len(exe_link) > 0 and 'beta' not in exe_link['href']:
                tor_exe_link=tor_url_base+exe_link['href'][2:]
                FRCAlert(tor_exe_link + '\n')

        for sig_link in tor_sig_links:
            if len(sig_link) > 0 and 'beta' not in sig_link['href']:
                tor_sig_link=tor_url_base+sig_link['href'][2:]
                FRCAlert(tor_sig_link + '\n')
        
        if len(tor_exe_link) == 0 or len(tor_sig_link) == 0:
            FRCAlert("Couldn't find download link for Tor.  Please tell whoever is running the Cryptoparty.\n")
            exit()
        FRCAlert('Found download links.  Downloading EXE from ' + tor_exe_link + '\n')
        tor_exe_file=requests.get(tor_exe_link,stream=True) 
        
        with open('tor.exe','wb') as f:
            for chunk in tor_exe_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('Downloaded exe.  Now downloading GPG signature from ' + tor_sig_link + '\n')
        tor_sig_file=requests.get(tor_sig_link)
        f=open('tor_sig.asc', 'wb')
        f.write(tor_sig_file.content)
        f.close()
        #And now to verify the executable.
        #I just hope that nobody tampered with both the exe AND the asc!
        #If they did, I'm going to download Erinn Clark's GPG off one of a list
        #of public key servers (from the Thunderbird defaults) and verify with
        #both keys.  If either one fails, I'll throw an exception.
        #TO-DO: Finish key verification
        try:
            gpg=gnupg.GPG()
            FRCAlert('Trying to download Tor devs GPG key\n')
            #TO-DO: Iterate through the standard servers in case sks-skyservers
            #is down.
            gpg.recv_keys('pool.sks-keyservers.net',tor_dev_gpg_fingerprint)
            f = open('tor_sig.asc','rb')
            #g = open('tor.exe','rb')
            FRCAlert('Verifying exe with GPG key in keyring\n')
            verified_with_asc = gpg.verify_file(f,os.path.abspath('tor.exe'))
            if verified_with_asc:
                FRCAlert("The Tor executable checks out.  Let's extract it.\n")
                os.system('tor.exe')
                f.close()
                #g.close()
            else:
                FRCAlert("EXE verification failed.  Please tell whoever is running your Cryptoparty." + '\n')
                f.close()
                #g.close()
                exit()
        except Exception as e:
            FRCAlert('Problem downloading Tor: Please show this to your facilitator: ' + unicode(e) + '\n')
    except Exception as e:
        printError(unicode(e))

def getThunderbird(lang):
    try:
        tbird_soup=BeautifulSoup(requests.get(thunderbird_url).content)
        tbird_link=tbird_soup.find_all('a',attrs={'href': re.compile('.*os=win.*lang=' + lang)})
        #print tbird_link
        tbird_file=requests.get(tbird_link[0]['href'],stream=True) 
        #Grease is the word...
        with open('thunderbird-installer.exe','wb') as f:
            for chunk in tbird_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        #I WOULD add signature verification code here, BUT THERE'S NO FUCKING
        #PGP key!
        os.system('thunderbird-installer.exe')
    except Exception as e:
        printError(unicode(e))

def getEnigmail(url):
    try:
        FRCAlert('in getEnigmail\n')
        enigmail_page = requests.get(url).content
        enigmail_soup = BeautifulSoup(enigmail_page)
        enigmail_links=enigmail_soup.find_all('a', attrs={'href': re.compile('enigmail.*sm\\+tb\\.xpi')})[:2]
        FRCAlert('contents of enigmail_links: ' + str(enigmail_links) + '\n')
        enigmail_xpi=requests.get(enigmail_links[0]['href'])
        FRCAlert('Downloaded enigmail.xpi\n')
        enigmail_asc=requests.get(HTTPSthis(enigmail_links[1]['href']))
        FRCAlert('scraped and downloaded enigmail\n')
        f = open('enigmail.xpi','wb')
        g = open('enigmail.xpi.asc','wb')
        f.write(enigmail_xpi.content)
        g.write(enigmail_asc.content)
        f.close()
        g.close()
        gpg=gnupg.GPG()    
		#TO-DO: Iterate through the standard servers in case sks-skyservers
        #is down.
        gpg.recv_keys('pool.sks-keyservers.net',enigmail_dev_gpg_fingerprint)
        x = open('enigmail.xpi.asc','rb')
        dd = os.path.abspath('enigmail.xpi')
        FRCAlert('Directory: ' + str(dd) + '\n')
        verified = gpg.verify_file(x,os.path.abspath('enigmail.xpi'))
        if verified:
            FRCAlert("The Enigmail plugin checks out.  Let's install it in Thunderbird\n")
            x.close()
        else:
            FRCAlert("Enigmail verification failed.  Please tell whoever is running your Cryptoparty.\n")
            x.close()
            exit()
    except Exception as e:
        printError(unicode(e))

def getTorBirdy():
    try:
        FRCAlert('in getTorBirdy\n')
        torbirdy_xpi=requests.get(torbirdy_xpi_url)
        FRCAlert('Downloaded torbirdy.xpi\n')
        torbirdy_asc=requests.get(torbirdy_xpi_sig_url)
        FRCAlert('Downloaded TorBirdy signature\n')
        f = open('torbirdy.xpi','wb')
        g = open('torbirdy.xpi.asc','wb')
        f.write(torbirdy_xpi.content)
        g.write(torbirdy_asc.content)
        f.close()
        g.close()
        gpg=gnupg.GPG()    
		#TO-DO: Iterate through the standard servers in case sks-skyservers
        #is down.
        gpg.recv_keys('pool.sks-keyservers.net',torbirdy_dev_gpg_fingerprint)
        x = open('torbirdy.xpi.asc','rb')
        dd = os.path.abspath('torbirdy.xpi')
        FRCAlert('Directory: ' + str(dd) + '\n')
        verified = gpg.verify_file(x,os.path.abspath('torbirdy.xpi'))
        if verified:
            FRCAlert("The Torbirdy plugin checks out.  Let's install it in Thunderbird\n")
            x.close()
        else:
            FRCAlert("Torbirdy verification failed.  Please tell whoever is running your Cryptoparty.\n")
            x.close()
            exit()
    except Exception as e:
        printError(unicode(e))



#def spaceEscape(d): #That's a fun NES game
#    return d.replace(' ','\ ')

def installEnigmail(start_after_copied):
    try:
        FRCAlert('Determined Thunderbird extensions directory: ' + thunderbird_ext_dir + '\n')
        FRCAlert('Determined Thunderbird main directory: ' + thunderbird_main_dir + '\n')
        copyfile(os.getcwd() + '\\' + 'enigmail.xpi', thunderbird_ext_dir + 'enigmail.xpi')
        xpi_id = processXpi(thunderbird_ext_dir + 'enigmail.xpi', thunderbird_ext_dir)['id']
        FRCAlert('Modifying registry\n')
        with CreateKey(HKEY_LOCAL_MACHINE,tbird_reg_str) as key:
            SetValueEx(key,"{3550f703-e582-4d05-9a08-453d09bdfdc6}",0,REG_SZ,xpi_id)
            FRCAlert('Set key in registry\n')
            CloseKey(key)
        FRCAlert('Starting Thunderbird\n')
        if start_after_copied:
            os.system(thunderbird_main_dir)
    except Exception as e:
        printError(unicode(e))

def installTorBirdy():
    try:
        FRCAlert('Determined Thunderbird extensions directory: ' + thunderbird_ext_dir + '\n')
        FRCAlert('Determined Thunderbird main directory: ' + thunderbird_main_dir + '\n')
        copyfile(os.getcwd() + '\\' + 'torbirdy.xpi', thunderbird_ext_dir + 'torbirdy.xpi')
        xpi_id = processXpi(thunderbird_ext_dir + 'torbirdy.xpi', thunderbird_ext_dir)['id']
        FRCAlert('Modifying registry\n')
        with CreateKey(HKEY_LOCAL_MACHINE,tbird_reg_str) as key:
           SetValueEx(key,"{3550f703-e582-4d05-9a08-453d09bdfdc6}",0,REG_SZ,xpi_id)
           FRCAlert('Set key in registry\n')
           CloseKey(key)
        FRCAlert('Starting Thunderbird\n')
        os.system(thunderbird_main_dir)
    except Exception as e:
        printError(unicode(e))


def getJitsi(url):
    try:
        FRCAlert('In getJitsi\n')
        jitsi_page = requests.get(url).content
        jitsi_soup = BeautifulSoup(jitsi_page)
        if arch == 32:
            jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/windows\\/jitsi-.*x86\\.exe$')})
        else:
            jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/windows\\/jitsi-.*x64\\.exe$')})
        FRCAlert('Starting installer download\n')
        jitsi_exe=requests.get(jitsi_links[0]['href'])
        FRCAlert('Jitsi download complete\n')
        with open('jitsi-installer.exe','wb') as f:
            for chunk in jitsi_exe.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        #I WOULD put GPG signature verification code here, but SOMEBODY didn't add a .asc!
        FRCAlert('Running installer\n')
        os.system('jitsi-installer.exe')
    except Exception as e:
        printError(e)
	
def getThunderbirdWithEnigmail(lang, start_after_copied):
    getThunderbird(lang)
    getEnigmail(enigmail_url)
    installEnigmail(start_after_copied)

#What's a good browser decision here?  Should I just install Firefox if it isn't installed, or add it to the TBB?
def getCryptoCat():
    pass

def getBleachBit():
    pass

def getTrueCrypt():
    pass

def getTailsISO():
    pass

def getFakeOut():
    pass


