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
#from _winreg import *

import wx

#TO-DO: Generic alert function.  Right now it just prints to stdout, but
#in later functions we should change this to something a little more
#user-friendly.
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
#Anyway, this function downloads and installs GPG.  It also checks the SHA1 checksum
#to make sure that it matches the signature on the download page.
def getGPG(url):
    print url
    gpg_page=requests.get(url)
    gpg4win_soup = BeautifulSoup(gpg_page.content, "lxml")
    #print gpg_page.content
    #We need to get the download link for the specific version of GPG we're trying to download.
    #For example, in the OSX version, the Intevation website has a link in the source code
    #like so: 
    #
    #    <a href="http://files.gpg4win.org/gpg4win-vanilla-2.2.1.exe">...</a>
    #
    #What the next line does is search for all the anchor links in the page, find and return the first href 
    #attribute that matches the regex "gpg4win-vanilla.*exe$".
    gpg4win_link=gpg4win_soup.find_all('a', attrs={'href': re.compile('gpg4win-vanilla.*exe$')})[0]['href']
    #I was lazy and didn't feel like walking a few tags down to get to the right <code> tag, so I just grabbed them all.
    #This should give us a list of 4 SHA1 checksums, one of whichd better match the EXE we're about to download.
    gpg4win_checksums=gpg4win_soup.find_all('code')
    #Download the exe, but stream it so that we can write it first to memory and then to disk as it comes in.
    gpg4win_file=requests.get(gpg4win_link,stream=True) 
    with open('gpg4win.exe','wb') as f:
        #Open up a file in write-binary mode and start reading in the file from the network 1024 bytes at a time.
        #Note that this is probably unnecessary for a file as small as GPG4Win on most computers, but something like the 
        #Tails ISO will make this necessary.
        for chunk in gpg4win_file.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                #write to disk
                f.write(chunk)
                f.flush()
	f.close()
    FRCAlert("Calculating and verifying SHA1, which is geek speak for making sure that nobody changed the file during download.\n")
    #Set up and compute the SHA1 of the fule we just downloaded
    sha1 = hashlib.sha1()
    f = open('gpg4win.exe','rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    gpg4win_hash = sha1.hexdigest()
    checksum_verified=False
    #Check to make sure it matches a signature from the page
    for checksum in gpg4win_checksums:
        if gpg4win_hash in checksum:
            FRCAlert("SHA1 verified, running installer\n")
            checksum_verified=True
            os.system("gpg4win.exe")
    if checksum_verified == False:
        #And if somebody is messing with the user's download, we should at least make them laugh.
        FRCAlert("SHA1 verification failed!  Hide yo kids!  Hide yo wife!  They messin' with everybody out here!\n")

#Debug code going on historical code now.
#Checks to make sure GPG is installed, and installs it if it isn't.
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
#Exception handler used in a few cases elsewhere in the code
def printError(text):
    print 'An error occured with your download.  Please show this to your Cruptoparty facilitator: ' + str(text)


#REQUIRE: url and lang are unicode
#Downloads and verifies Tor given a URL and language tag
#Examples of the language tag include: 
#  'en-us'
#  'ar'
#  'de'
#  'fr'
#  'es-ES'
def getTOR(url, lang):	
    try:
        #get and parse the HTML of the download page
        tor_page=requests.get(url)
        tor_soup = BeautifulSoup(tor_page.content, "lxml")
        tor_exe_link=''
        tor_sig_link=''
        FRCAlert('Scraping the Tor Project site for the relevant links\n')
        #Find the anchor tags for the language's EXE and OpenPGP signature
        tor_link_exes=tor_soup.find_all('a', attrs={'href': re.compile('torbrowser-install-.*' + lang + '.*exe$')})
        tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('torbrowser-install-.*' + lang + '\\.exe\\.*asc$')})
        #We parse the url and add the scheme because the href text in the source looks something like this:
        # ../dist/torbrowser/3.5.2.1/torbrowser-install-3.5.2.1_vi.exe
        #Therefore we need to take the url in the href attribute,  parse out the netloc, and add https to the beginning.
        tor_url_parsed=urlparse(url)
        tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc
        
        #print unicode(tor_link_exes) + '\n\n' + unicode(tor_sig_links)
        #In an earlier version of the Tor download page, the stable version
        #and the beta version were available and localized to American English,
        #Hence the two for loops below to find the non-beta version.
        #TO-DO: Remove the for loops to make the code more readable.
        for exe_link in tor_link_exes:
            if len(exe_link) > 0 and 'beta' not in exe_link['href']:
                tor_exe_link=tor_url_base+exe_link['href'][2:]
                FRCAlert(tor_exe_link + '\n')

        for sig_link in tor_sig_links:
            if len(sig_link) > 0 and 'beta' not in sig_link['href']:
                tor_sig_link=tor_url_base+sig_link['href'][2:]
                FRCAlert(tor_sig_link + '\n')
        #Check to make sure we have an exe link and a signature link
        #to request.
        if len(tor_exe_link) == 0 or len(tor_sig_link) == 0:
            FRCAlert("Couldn't find download link for Tor.  Please tell whoever is running the Cryptoparty.\n")
            exit()
        FRCAlert('Found download links.  Downloading EXE from ' + tor_exe_link + '\n')
        #Download and write to file (see getGPG for an explanation of the with block below
        tor_exe_file=requests.get(tor_exe_link,stream=True) 
        with open('tor.exe','wb') as f:
            for chunk in tor_exe_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('Downloaded exe.  Now downloading GPG signature from ' + tor_sig_link + '\n')
        #Now download the signature
        tor_sig_file=requests.get(tor_sig_link)
        f=open('tor_sig.asc', 'wb')
        f.write(tor_sig_file.content)
        f.close()
        #And now to verify the executable.
        #I just hope that nobody tampered with both the exe AND the asc!
        #If they did, I'm going to download Erinn Clark's GPG off one of a list
        #of public key servers (from the Thunderbird defaults) and verify with
        #both keys.  If either one fails, I'll throw an exception.
        #TO-DO: Tweak the key verification.  It might be a good idea to use
        #a server that speaks HKPS if we can find one.
        try:
            #Start up GPG
            gpg=gnupg.GPG()
            FRCAlert('Trying to download Tor devs GPG key\n')
            #TO-DO: Iterate through the standard servers in case sks-skyservers
            #is down.
            #gpg.recv_keys('pool.sks-keyservers.net',tor_dev_gpg_fingerprint)
            f = open('tor_sig.asc','rb')
            #g = open('tor.exe','rb')
            FRCAlert('Verifying exe with GPG key in keyring\n')
            verified_with_asc = gpg.verify_file(open(os.path.abspath('tor.exe')), 'tor_sig.asc')
            if verified_with_asc:
                FRCAlert("The Tor executable checks out.  Let's extract it.\n")
                os.system('tor.exe')
                f.close()
                #g.close()
            else:
                FRCAlert("EXE verification failed.  Please tell whoever is running your Cryptoparty." + "\n")
                f.close()
                #g.close()
                exit()
        except Exception as e:
            FRCAlert('Problem downloading Tor: Please show this to your facilitator: ' + unicode(e) + '\n')
    except Exception as e:
        printError(unicode(e))

#Downloads the Thunderbird installer for Windows and runs it.
def getThunderbird(lang):
    try:
        #Get the HTML and parse out the link for the language we want
        tbird_soup=BeautifulSoup(requests.get(thunderbird_url).content, "lxml")
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
        #I WOULD add signature verification code here, BUT THERE'S NO FSCKING
        #PGP key!
        os.system('thunderbird-installer.exe')
    except Exception as e:
        printError(unicode(e))

#Download the XPI file (standard file for Thunderbird/Icedove and Firefox/Iceweasel plugins)
#for Enigmail.  See installEnigmail() for the installation step.
def getEnigmail(url):
    try:
        FRCAlert('in getEnigmail\n')
        #Lather, rinse, repeat I mean get, scrape, repeat
        enigmail_page = requests.get(url).content
        enigmail_soup = BeautifulSoup(enigmail_page, "lxml")
        enigmail_links=enigmail_soup.find_all('a', attrs={'href': re.compile('enigmail.*sm\\+tb\\.xpi')})[:2]
        #FRCAlert('contents of enigmail_links: ' + enigmail_links[0]['href'] + '\n')
        enigmail_xpi=requests.get(enigmail_links[0]['href'])
        FRCAlert('Downloaded enigmail.xpi\n')
        enigmail_asc=requests.get(enigmail_links[1]['href'])
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
        #gpg.recv_keys('pool.sks-keyservers.net',enigmail_dev_gpg_fingerprint)
        x = open('enigmail.xpi.asc','rb')
        dd = os.path.abspath('enigmail.xpi')
        FRCAlert('Directory: ' + str(dd) + '\n')
        verified = gpg.verify_file(open(dd),os.path.abspath('enigmail.xpi.asc'))
        print verified.stderr
        if verified:
            FRCAlert("The Enigmail plugin checks out.  Let's install it in Thunderbird\n")
            x.close()
        else:
            FRCAlert("Enigmail verification failed.  Please tell whoever is running your Cryptoparty.\n")
            x.close()
            exit()
    except Exception as e:
        printError(unicode(e))

#Download the XPI file (standard file for Thunderbird/Icedove and Firefox/Iceweasel plugins)
#for TorBirdy.  See installTorBirdy for the installation step.
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
        gpg.recv_keys('pgp.mit.edu','0x744301A2')
        x = open('torbirdy.xpi.asc','rb')
        dd = os.path.abspath('torbirdy.xpi')
        FRCAlert('Directory: ' + str(dd) + '\n')
        verified = gpg.verify_file(open(dd), os.path.abspath('torbirdy.xpi.asc'))
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

#installEnigmail: Copies the Enigmail XPI to the appropriate Thunderbird directory, decompresses it then
#modifies the registry so that thunderbird knows there's a new plugin to be installed 
#see https://developer.mozilla.org/en-US/docs/Adding_Extensions_using_the_Windows_Registry
#for an explanation
###################
#start_after_copied: If true, restart Thunderbird after the plugin is copied
#(so that it adds it automatically)
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

#Same as installEnigmail(), but installs the TorBirdy plugin and doesn't have the
#start_after_copied argument
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

#Downloads and installs Jitsi.  Unfortunately, no OpenPGP signature is available at this time
def getJitsi(url):
    try:
        FRCAlert('In getJitsi\n')
        jitsi_page = requests.get(url).content
        jitsi_soup = BeautifulSoup(jitsi_page, "lxml")
        #Since Jitsi is available for both 32 and 64-bit Windows, we make a decision about which link to 
        #scrape based on the architecture of the system, which we determine in frc_winconfig.py
        if arch == 32:
            jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/windows\\/jitsi-.*x86\\.exe$')})
        else:
            jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/windows\\/jitsi-.*x64\\.exe$')})
        FRCAlert('Starting installer download\n')
        #Download and write to file
        #TO-DO: make the get request with stream=True
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

#Master function to handle the download, verification, and install steps
#for Thunderbird and Enigmail.
def getThunderbirdWithEnigmail(lang, start_after_copied):
    getThunderbird(lang)
    getEnigmail(enigmail_url)
    installEnigmail(start_after_copied)

#[2/3]What's a good browser decision here?  Should I just install Firefox if it isn't installed, or add it to the TBB?
def getCryptoCat():
    pass

#[1]Straight HTTP download.  Does offer a sha256 sum over HTTP.
def getBleachBit():
    try:
        bleachbit_soup = BeautifulSoup(requests.get(bleachbit_url).content, "lxml")
        bleachbit_exe_link = bleachbit_soup.find_all('a', attrs = {'href': re.compile('BleachBit-.*\\.exe$')})[0]['href']
        FRCAlert('Found download links: ' + str(bleachbit_exe_link))
        bleachbit_exe = requests.get(bleachbit_base_url + bleachbit_exe_link)
        with open('bleachbit-installer.exe','wb') as f:
            for chunk in bleachbit_exe.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('Bleachbit EXE written to disk.  Running installer.')
        os.system('bleachbit-installer.exe')
    except Exception as e:
        printError(e)
    

#[4]Weird POST and transient URL stuff here, HTTP but there is PGP sig
def getTrueCrypt():
    FRCAlert('TrueCrypt download stub here.')

#[5]Big HTTPS download, but there is a signature over HTTP
def getTailsISO():
    tails_soup = BeautifulSoup(requests.get(tails_url).content, "lxml")
    tails_iso_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso$')})[0]['href']
    FRCAlert('Got Tails download link: ' + str(tails_iso_link))
    tails_sig_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso\\.sig$')})[0]['href']

def downloadFakeOut():
    try:
        fakeout_soup = BeautifulSoup(requests.get(fakeout_url).content, "lxml")
        fakeout_xpi_link = fakeout_soup.find_all('a', attrs = {'href': re.compile('fake_domain_detective_plugin.8\\.xpi')})[0]['href']
        FRCAlert('Found download links: ' + str(fakeout_xpi_link))
        fakeout_xpi = requests.get(fakeout_xpi_link).content
        with open('fakeout.xpi','wb') as f:
            for chunk in fakeout_xpi.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('FakeOut EXE written to disk.  Running installer.')
        #Coming soon: A detached GPG signature for this so we can verify the integrity.
    except Exception as e:
        printError(e)

def installFakeOut():
    pass
#Copied and pasted the TorBirdy install code.  
#Need to figure out if there are any significant changes needed.
#    try:
#        FRCAlert('Determined Thunderbird extensions directory: ' + thunderbird_ext_dir + '\n')
#        FRCAlert('Determined Thunderbird main directory: ' + thunderbird_main_dir + '\n')
#        copyfile(os.getcwd() + '\\' + 'fakeout.xpi', thunderbird_ext_dir + 'fakeout.xpi')
#        xpi_id = processXpi(thunderbird_ext_dir + 'fakeout.xpi', thunderbird_ext_dir)['id']
#        FRCAlert('Modifying registry\n')
#        with CreateKey(HKEY_LOCAL_MACHINE,tbird_reg_str) as key:
#           SetValueEx(key,"{3550f703-e582-4d05-9a08-453d09bdfdc6}",0,REG_SZ,xpi_id)
#           FRCAlert('Set key in registry\n')
#          CloseKey(key)
#        FRCAlert('Starting Thunderbird\n')
#        os.system(thunderbird_main_dir)
#    except Exception as e:
#        printError(unicode(e))

#[2/3]HTTPS download, PGP signature coming soon
def getFakeOut():
    downloadFakeOut()
    installFakeOut()

