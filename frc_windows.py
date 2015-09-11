# Copyright (C) 2013-2015 Access Organistion.
# See the file 'LICENSE' for copying permission.
#
# This file contains the functions that used to download, verify
# and install tools.


import os
import requests
import re
import hashlib
import wx
from shutil import copyfile
from bs4 import BeautifulSoup
from urlparse import urlparse
from frc_winconfig import *
from xpi2folders import *

def FRCAlert(text):
     print text

# This function downloads and installs GPG program
def getGPG(url):
    print url
    gpg_page=requests.get(url)
    gpg4win_soup = BeautifulSoup(gpg_page.content, "lxml")
    gpg4win_link=gpg4win_soup.find_all('a', attrs={'href': re.compile('gpg4win-vanilla.*exe$')})[0]['href']
    gpg4win_checksums=gpg4win_soup.find_all('code')
    gpg4win_file=requests.get(gpg4win_link,stream=True) 
    with open('gpg4win.exe','wb') as f:
        for chunk in gpg4win_file.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
                f.flush()
	f.close()
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
    gpg=gnupg.GPG()
except Exception:
    FRCAlert("GnuPG not found.  Downloading it now.\n")
    FRCAlert("Expect an installer window in 5 minutes.\n")
    getGPG(gpg4win_url)
    import gnupg

def httpsThis(url):
    return re.sub(pattern='http', repl='https', string=url)

def printError(text):
    print 'An error occured with your download.  Please show this to your Cruptoparty facilitator: ' + str(text)

# This function downloads and installs the Tor browser bundle 
def getTOR(url, lang):	
    try:
        # Get and parse the HTML of the download page
        tor_page=requests.get(url)
        tor_soup = BeautifulSoup(tor_page.content, "lxml")
        tor_exe_link=''
        tor_sig_link=''
        FRCAlert('Scraping the Tor Project site for the relevant links\n')
        # Find the anchor tags for the language's EXE and OpenPGP signature
        tor_link_exes=tor_soup.find_all('a', attrs={'href': re.compile('torbrowser-install-.*' + lang + '.*exe$')})
        tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('torbrowser-install-.*' + lang + '\\.exe\\.*asc$')})
        tor_url_parsed=urlparse(url)
        tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc        
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
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('Downloaded exe.  Now downloading GPG signature from ' + tor_sig_link + '\n')
        # Now download the signature
        tor_sig_file=requests.get(tor_sig_link)
        f=open('tor_sig.asc', 'wb')
        f.write(tor_sig_file.content)
        f.close()
        try:
            gpg=gnupg.GPG()
            FRCAlert('Trying to download Tor devs GPG key\n')
            f = open('tor_sig.asc','rb')
            FRCAlert('Verifying exe with GPG key in keyring\n')
            verified_with_asc = gpg.verify_file(open(os.path.abspath('tor.exe')), 'tor_sig.asc')
            if verified_with_asc:
                FRCAlert("The Tor executable checks out.  Let's extract it.\n")
                os.system('tor.exe')
                f.close()
            else:
                FRCAlert("EXE verification failed.  Please tell whoever is running your Cryptoparty." + "\n")
                f.close()
                exit()
        except Exception as e:
            FRCAlert('Problem downloading Tor: Please show this to your facilitator: ' + unicode(e) + '\n')
    except Exception as e:
        printError(unicode(e))

# This function downloafs and installs Thunderbird
def getThunderbird(lang):
    try:
        # Get the HTML and parse out the link for the language we want
        tbird_soup=BeautifulSoup(requests.get(thunderbird_url).content, "lxml")
        tbird_link=tbird_soup.find_all('a',attrs={'href': re.compile('.*os=win.*lang=' + lang)})
        tbird_file=requests.get(tbird_link[0]['href'],stream=True) 
        with open('thunderbird-installer.exe','wb') as f:
            for chunk in tbird_file.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        os.system('thunderbird-installer.exe')
    except Exception as e:
        printError(unicode(e))

# This function downloads and verifies Thunderbird
def getEnigmail(url):
    try:
        FRCAlert('In getEnigmail\n')
        enigmail_page = requests.get(url).content
        enigmail_soup = BeautifulSoup(enigmail_page, "lxml")
        enigmail_links=enigmail_soup.find_all('a', attrs={'href': re.compile('enigmail.*sm\\+tb\\.xpi')})[:2]
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

# This function downloads and verifies Torbirdy
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

# This function downloads and verifies Torbirdy
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

# This function installs Torbirdy plugin
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

# This function downloads and installs Jitsi
def getJitsi(url):
    try:
        FRCAlert('In getJitsi\n')
        jitsi_page = requests.get(url).content
        jitsi_soup = BeautifulSoup(jitsi_page, "lxml")
        if arch == 32:
            jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/windows\\/jitsi-.*x86\\.exe$')})
        else:
            jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/windows\\/jitsi-.*x64\\.exe$')})
        FRCAlert('Starting installer download\n')
        jitsi_exe=requests.get(jitsi_links[0]['href'])
        FRCAlert('Jitsi download complete\n')
        with open('jitsi-installer.exe','wb') as f:
            for chunk in jitsi_exe.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('Running installer\n')
        os.system('jitsi-installer.exe')
    except Exception as e:
        printError(e)

# This function installs Thunderbird with Engimail
def getThunderbirdWithEnigmail(lang, start_after_copied):
    getThunderbird(lang)
    getEnigmail(enigmail_url)
    installEnigmail(start_after_copied)

# This function downloads Tails iso 
def getTailsISO():
    tails_soup = BeautifulSoup(requests.get(tails_url).content, "lxml")
    tails_iso_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso$')})[0]['href']
    FRCAlert('Got Tails download link: ' + str(tails_iso_link))
    tails_sig_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso\\.sig$')})[0]['href']

# This function downloads FakeOut plugin 
def downloadFakeOut():
    try:
        fakeout_soup = BeautifulSoup(requests.get(fakeout_url).content, "lxml")
        fakeout_xpi_link = fakeout_soup.find_all('a', attrs = {'href': re.compile('fake_domain_detective_plugin.8\\.xpi')})[0]['href']
        FRCAlert('Found download links: ' + str(fakeout_xpi_link))
        fakeout_xpi = requests.get(fakeout_xpi_link).content
        with open('fakeout.xpi','wb') as f:
            for chunk in fakeout_xpi.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        FRCAlert('FakeOut EXE written to disk.  Running installer.')
    except Exception as e:
        printError(e)

