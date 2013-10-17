#Fly Rod Crosby: Making Cryptoparties Easier since 1905!

import os
from bs4 import BeautifulSoup
#import wx
import requests
import re
import hashlib
from urlparse import urlparse
from frc-winconfig import *

#Intevation doesn't have an HTTPS download of the file 
#that doesn't throw a certificate error.  Could somebody yell at them, please?	
#Anyway 
def getGPG(url):
    gpg_page=requests.get(url)
    gpg4win_soup = BeautifulSoup(gpg_page.content)
    gpg4win_link=gpg4win_soup.find_all('a', attrs={'href': re.compile('gpg4win-light.*exe$')})[0]['href']
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
    gpg=gnupg.GPG()
except Exception:
    print "GnuPG not found.  Downloading it now."
    print "Expect an installer window in 5 minutes."
    getGPG(gpg4win_url)

try:
    gpg=gnupg.GPG()
    print 'GnuPG installed'
except Exception:
    print 'Ugh, turns out it doesnt update after installation'

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
        tor_link_exes=onion_soup.find_all('a', attrs={'href': re.compile('tor-browser.*' + lang + '.*exe$')})
		tor_sig_links=onion_soup.find_all('a', attrs={'href': re.compile('tor-browser.*' + lang + '.*asc$')})
        for exe_link, sig_link in map(None, tor_link_exes, tor_sig_exes):
            if len(exe_link) > 0 and 'beta' not in sig_link['href']:
                tor_exe_link=exe_link['href'][2:]
            if len(sig_link) > 0 and 'beta' not in exe_link['href']:
                tor_sig_link=sig_link['href'][2:]
        
		if len(tor_link) == 0 or len(tor_sig_link) == 0:
            print "Couldn't find download link for Tor.  Please tell whoever is running the Cryptoparty."
            exit()
        
        tor_exe_file=requests.get(url + tor_exe_link,stream=True) 
        with open('tor.exe','wb') as f:
            for chunk in tor_exe_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()

        tor_sig_file=requests.get(tor_sig_link)
        f=open('tor_sig.asc')
        f.write(tor_sig_file)
        f.close()
        #And now to verify the executable.
        #I just hope that nobody tampered with both the exe AND the asc!
        #If they did, I'm going to download Erinn Clark's GPG off one of a list
        #of public key servers (from the Thunderbird defaults) and verify with
        #both keys.  If either one fails, I'll throw an exception.
        #TO-DO: Finish key verification
        try:
            gpg=gnupg.GPG()
            gpg.recv_keys('pool.sks-keyservers.net',tor_dev_gpg_id)
			f = open('tor_sig.asc','rb')
            g = open('tor.exe','rb')
		    #This verifies the executable with the key in the keyring
            verified_exe_with_kring = gpg.verify(g)
            #This verifies the executable with the downloaded signature
			verified_with_asc = gpg.verify_file(f,os.path.abspath('tor.exe'))
			if verified_with_asc amd verified_exe:
                print "The Tor executable checks out.  Let's extract it."                
                os.system('tor.exe')
                f.close()
                g.close()
			elif verified_with_asc and not verified_exe_with_kring:
                print 'The signature checked out, but not the executable.  Game over.'
            elif verified_exe_with_kring and not verified_with_asc:
                print 'The executable has been verified, but the signature failed.  Game over.'
            else;
                print "Neither the signature nor the executable checked out.  Game over."
                f.close()
                g.close()
				exit()
        except Exception as e:
		    print 'Problem downloading Tor: Please show this to your facilitator: ' + unicode(e)
    except Exception as e:
        print 'An error occured with your Tor download.  Please show this message to your Cryptoparty facilitator: ' + unicode(e)
	
def getThunderbirdWithEnigmail():
    pass
#What's a good browser decision here?  Should I just install Firefox if it isn't installed, or add it to the TBB?
def getCryptocat():
    pass