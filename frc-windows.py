#Fly Rod Crosby: Making Cryptoparties Easier since 1905!

import os
import requests
import re
import hashlib
from shutil import copyfile
from bs4 import BeautifulSoup
from urlparse import urlparse
from frc_winconfig import *

#Given an HTTP url, return it with https
def HTTPSthis(url):
    return re.sub(pattern='http', repl='https', string=url)

def printError(text):
    print 'An error occured with your download.  Please show this to your Cruptoparty facilitator: ' + text

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
	print "Calculating and verifying SHA1, which is geek speak for making sure that nobody changed the file during download."
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
            print "SHA1 verified, running installer"
            checksum_verified=True
            os.system("gpg4win.exe")
    if checksum_verified == False:
        print "SHA1 verification failed!  Hide yo kids!  Hide yo wife!  The NSA messin' with everybody out here!"

try:
    import gnupg
    print 'near gpg init'
    gpg=gnupg.GPG()
    print 'after gpg init'
except Exception:
    print "GnuPG not found.  Downloading it now."
    print "Expect an installer window in 5 minutes."
    getGPG(gpg4win_url)

#REQUIRE: url and lang are unicode
def getTOR(url, lang):	
    try:
        tor_page=requests.get(url)
        tor_soup = BeautifulSoup(tor_page.content)
        tor_exe_link=''
        tor_sig_link=''
		
		#TO-DO: Alas my regex fu is too weak to filter out the beta version, 
        #so this will return two links.  
        #If somebody from the Tor Project is reading this, would it kill you to use absolute links?
        print 'Scraping the Tor Project site for the relevant links'
        tor_link_exes=tor_soup.find_all('a', attrs={'href': re.compile('tor-browser.*' + lang + '.*exe$')})
        tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('tor-browser.*' + lang + '\\.exe\\.*asc$')})
        tor_url_parsed=urlparse(url)
        tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc
        
        #print unicode(tor_link_exes) + '\n\n' + unicode(tor_sig_links)
        
        
        for exe_link in tor_link_exes:
            if len(exe_link) > 0 and 'beta' not in exe_link['href']:
                tor_exe_link=tor_url_base+exe_link['href'][2:]
                print tor_exe_link

        for sig_link in tor_sig_links:
            if len(sig_link) > 0 and 'beta' not in sig_link['href']:
                tor_sig_link=tor_url_base+sig_link['href'][2:]
                print tor_sig_link
        
        if len(tor_exe_link) == 0 or len(tor_sig_link) == 0:
            print "Couldn't find download link for Tor.  Please tell whoever is running the Cryptoparty."
            exit()
        print 'Found download links.  Downloading EXE from ' + tor_exe_link
        tor_exe_file=requests.get(tor_exe_link,stream=True) 
        
        with open('tor.exe','wb') as f:
            for chunk in tor_exe_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        print 'Downloaded exe.  Now downloading GPG signature from' + tor_sig_link
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
            print 'Trying to download Tor devs GPG key'
            gpg.recv_keys('pool.sks-keyservers.net',tor_dev_gpg_id)
            f = open('tor_sig.asc','rb')
            #g = open('tor.exe','rb')
            print 'Verifying exe with GPG key in keyring'
            verified_with_asc = gpg.verify_file(f,os.path.abspath('tor.exe'))
            if verified_with_asc:
                print "The Tor executable checks out.  Let's extract it."                
                os.system('tor.exe')
                f.close()
                #g.close()
            else:
                print "EXE verification failed.  Please tell whoever is running your Cryptoparty."
                f.close()
                #g.close()
                exit()
        except Exception as e:
            print 'Problem downloading Tor: Please show this to your facilitator: ' + unicode(e)
    except Exception as e:
        printError(unicode(e))

def getThunderbird(lang):
    try:
        tbird_soup=BeautifulSoup(requests.get(thunderbird_url).content)
        tbird_link=tbird_soup.find_all('a',attrs={'href': re.compile('.*os=win.*lang=' + lang)})
        #print tbird_link
        tbird_file=requests.get(tbird_link[0]['href'],stream=True) 
        #Grease is the word...
        with open('thunderbird.exe','wb') as f:
            for chunk in tbird_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        #I WOULD add signature verification code here, BUT THERE'S NO FUCKING
        #PGP key!
        os.system('thunderbird.exe')
    except Exception as e:
        printError(unicode(e))

def getEnigmail(url):
    try:
        print 'in getEnigmail'
        enigmail_page = requests.get(url).content
        enigmail_soup = BeautifulSoup(enigmail_page)
        enigmail_links=enigmail_soup.find_all('a', attrs={'href': re.compile('enigmail.*sm\\+tb\\.xpi')})[:2]
        print 'contents of enigmail_links: ' + str(enigmail_links)
        enigmail_xpi=requests.get(enigmail_links[0]['href'])
        print 'Downloaded enigmail.xpi'
        enigmail_asc=requests.get(HTTPSthis(enigmail_links[1]['href']))
        print 'scraped and downloaded enigmail'
        f = open('enigmail.xpi','wb')
        g = open('enigmail.xpi.asc','wb')
        f.write(enigmail_xpi.content)
        g.write(enigmail_asc.content)
        f.close()
        g.close()
        gpg=gnupg.GPG()    
        gpg.recv_keys('pool.sks-keyservers.net',enigmail_dev_gpg_id)
        x = open('enigmail.xpi.asc','rb')
        dd = os.path.abspath('enigmail.xpi')
        print 'Directory: ' + str(dd)
        verified = gpg.verify_file(x,os.path.abspath('enigmail.xpi'))
        if verified:
            print "The Enigmail plugin checks out.  Let's install it in Thunderbird"
            x.close()
        else:
            print "Enigmail verification failed.  Please tell whoever is running your Cryptoparty."
            x.close()
            exit()
    except Exception as e:
        printError(unicode(e))

def spaceEscape(d): #That's a fun NES game
    return d.replace(' ','\ ')

def installEnigmail():
    try:
        for d in thunderbird_extensions_dirs:
            if os.path.isdir(d):
                thunderbird_ext_dir=d
        for d in thunderbird_dirs:
            if os.path.isdir(d):
                thunderbird_main_dir=d		
        print 'Determined Thunderbird extensions directory: ' + thunderbird_ext_dir
        print 'Determined Thunderbird main directory: ' + thunderbird_main_dir
        copyfile('enigmail.xpi',thunderbird_ext_dir + 'enigmail.xpi')
        os.system(spaceEscape(thunderbird_main_dir) + 'thunderbird.exe')
    except Exception as e:
        printError(unicode(e))

def getJitsi():
    pass

def getThunderbirdWithEnigmail(lang):
    getThunderbird(lang)
    getEnigmail(enigmail_url)
    installEnigmail()

#What's a good browser decision here?  Should I just install Firefox if it isn't installed, or add it to the TBB?
def getCryptoCat():
    pass

#getTOR(tor_url,'en-US')
#getEnigmail(enigmail_url)
getThunderbirdWithEnigmail('en-US')