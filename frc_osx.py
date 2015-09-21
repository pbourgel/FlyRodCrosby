#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc_osx.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the functions used to download,
#                   verify and install the different tools.
###########################################################################

import os
import requests
import re
import hashlib
import urllib , urllib2
import zipfile		
from shutil import copyfile
from bs4 import BeautifulSoup
from urlparse import urlparse
from xml.dom import minidom

from frc_osxconfig import *

# This function installs the given plugin into Firefox
def installFirefoxPlugin(plugin_name):
  os.system("rm install.rdf")
  task="unzip -p "+plugin_name+" install.rdf > install.rdf"
  os.system(task)
  xmldoc = minidom.parse("install.rdf")
  dom = minidom.parseString(xmldoc.toxml())
  plugin_id = str(dom.getElementsByTagName("em:id")[0].toxml().replace('<em:id>','').replace('</em:id>',''))
  for x in os.listdir(home+ "/Library/Application Support/Firefox/Profiles"):
	  if x.endswith(".default"):
		  profile=x
	          break
  path=home + "/Library/Application\ Support/Firefox/Profiles/"+profile+"/extensions/" 
  path=path +plugin_id+ ".xpi " 
  task = " cp " +plugin_name+ " " +path
  os.system(task)

def installPlugin(plugin_name):
  task="unzip -p "+plugin_name+" install.rdf > install.rdf"
  os.system(task)
  xmldoc = minidom.parse("install.rdf")
  dom = minidom.parseString(xmldoc.toxml())
  plugin_id = str(dom.getElementsByTagName("em:id")[0].toxml().replace('<em:id>','').replace('</em:id>',''))
  profile = ""
  for x in os.listdir(home + "/Library/Thunderbird/Profiles/"):
	  if x.endswith(".default"):
		  profile=x
		  break

  path=home+"/Library/Thunderbird/Profiles/"+profile+"/extensions.ini"
  fd = open(path,"r")
  lines  = [i for i  in fd]
  fd.close()

  path=home+"/Library/Thunderbird/Profiles/"+profile+"/extensions/"   
  path=path +plugin_id
  
  d= 'Extension'+Word(nums)+Word(alphas + nums + '/'+'=')  
  i = 0
  for line in lines:
	i= i+1
	if line  == "[ExtensionDirs]\r\n":
		if lines[i] == "\r\n":
			lines.insert(i, "Extension0=" +path+"\r\n\r\n")
		elif line.startswith("Extension"):
           		rang = int(d.parseString(line)[1])+1
			lines.insert(i+1,"Extension"+str(rang)+path+"\r\n\r\n")
		
		break
  path2=home+"/Library/Thunderbird/Profiles/"+profile+"/extensions.ini"
  fd=open(path2, "w")
  for line in lines:
    fd.write(line)

  fd.close()
  
  
  path=path +"/" 
  file=zipfile.ZipFile(plugin_name)
  file.extractall(path)

def FRCAlert(text):
     print text

# This function downloads and installs GPG program
def getGPG(macGPGurl):	
  page = requests.get(macGPGurl,verify=False)
  soup = BeautifulSoup(page.content)
  link=soup.find_all('a',attrs={'href': re.compile("GPG%20Suite *")}) [0]['href'] 
  macGPG_file=requests.get(link,stream=True,verify=False)
  with open('./%s' % "GPG_Suite.dmg",'wb') as f:
   print "The GPG Suite Tools is downloading..\n"
   for chunk in macGPG_file.iter_content(chunk_size=1024):
     if chunk:
       f.write(chunk)
       f.flush
   f.close()
  os.system("open GPG_Suite.dmg")
    
try:
    import gnupg
    gpg=gnupg.GPG()
except Exception:
    FRCAlert("GnuPG not found.  Downloading it now.\n")
    FRCAlert("Expect an installer window in 5 minutes.\n")
    getGPG(macGPGurl)
    import gnupg

def httpThis(url):
    return re.sub(pattern='http', repl='https', string=url)

def printError(text):
    print 'An error occured with your download.  Please show this to your Cryptoparty facilitator: ' + str(text)
    print "ERROR: "+ str(text)

# This function downloads and installs the Tor browser bundle
def getTOR(url,lang):	
    try:
        # Get and parse the HTML of the download page
        tor_page=requests.get(url)
        tor_ascii_text = BeautifulSoup(tor_page.content)
        tor_zip_link=''
        tor_sig_links=''
        FRCAlert('Scraping the Tor Project site for the relevant links\n')
        # Find the anchor tags for the language's EXE and OpenPGP signature
        tor_zip_link=tor_ascii_text.find_all('a', attrs={'href': re.compile('/TorBrowser.*.'+lang+'.*.')})[0]['href'][2:]
        tor_sig_links=tor_ascii_text.find_all('a', attrs={'href': re.compile('/TorBrowser.*.'+lang+'.*.')})[1]['href'][2:]          
        tor_url_parsed=urlparse(url)
        tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc
        if len(tor_zip_link) == 0 or len(tor_sig_links) == 0:
            FRCAlert("Couldn't find download link for Tor.  Please tell whoever is running the Cryptoparty.\n")
            exit()
        FRCAlert('Found download links.  Downloading the zip from ' + tor_zip_link + '\n')
        tor_zip_link=tor_url_base+tor_zip_link	
        tor_zip_file=requests.get(tor_zip_link,stream=True) 
	with open('tor.dmg','wb') as f:
            for chunk in tor_zip_file.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        tor_sig_links=tor_url_base+tor_sig_links
        FRCAlert('Downloaded .dmg  Now downloading GPG signature from ' + tor_sig_links + '\n')
        tor_sig_file=requests.get(tor_sig_links)
        f=open('tor_sig.asc', 'wb')
        f.write(tor_sig_file.content)
        f.close()        
        try:
            gpg=gnupg.GPG()
            FRCAlert('Trying to download Tor devs GPG key\n')
            #TO-DO: Iterate through the standard servers in case sks-skyservers
            #is down.
            gpg.recv_keys('pool.sks-keyservers.net',tor_dev_gpg_fingerprint)
            f = open('tor_sig.asc','rb')
            FRCAlert('Verifying exe with GPG key in keyring\n')
            verified_with_asc = gpg.verify_file(f,os.path.abspath('tor.dmg'))
            if verified_with_asc:
                FRCAlert("The Tor executable checks out.  Let's open it.\n")
                os.system('open tor.dmg')
                f.close()             
            else:
                FRCAlert(".dmg verification failed.  Please tell whoever is running your Cryptoparty." + "\n")
                f.close()
                exit()
        except Exception as e:
            FRCAlert('Problem downloading Tor: Please show this to your facilitator: ' + unicode(e) + '\n')
    except Exception as e:
        print unicode(e)

# This function installs Thunderbird 
def getThunderbird(lang):
    try:
        tbird_ascii_text=BeautifulSoup(requests.get(thunderbird_url).content)#here we go very fast :p
        tbird_link=tbird_ascii_text.find_all('a',attrs={'href': re.compile('.*os=osx.*lang=' + lang)})
        tbird_file=requests.get(tbird_link[0]['href'],stream=True)
        with open('thunderbird-installer.dmg','wb') as f:
            for chunk in tbird_file.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
        f.close()
        os.system('open thunderbird-installer.dmg')
        print('Thunderbird is ready let\'s install enigmail')
    except Exception as e:
        printError(unicode(e))

# This function Downloads Engimail plugin
def getEnigmail(url):
    try:
	RCAlert('in getEnigmail\n')
        enigmail_page = requests.get(url).content
        enigmail_ascii_text = BeautifulSoup(enigmail_page)
        enigmail_links=enigmail_ascii_text.find_all('a', attrs={'href': re.compile('enigmail-1.7.*-tb\\+sm\\.xpi')})[:2]
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
		FRCAlert("The Enigmail plugin checks out. Let's install it in Thunderbird\n")
		x.close()
        else:
		FRCAlert("Enigmail verification failed. Please tell whoever is running your Cryptoparty.\n")
		x.close()
		exit()
    except Exception as e:
        printError(unicode(e))

# This function Downloads Torbirdy plugin
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

# This function installs Engimail plugin
def installEnigmail():
    try:
    	installPlugin("enigmail17.xpi")
    except Exception as e:
     	printError(unicode(e))

# This function installs Torbirdy plugin
def installTorBirdy():
    try:
	installPlugin("torbirdy.xpi")
    except Exception as e:
	printError(unicode(e))

# This function downloads and installs Jitsi
def getJitsi(url):
    try:
      FRCAlert('In getJitsi\n')
      jitsi_page = requests.get(url).content
      jitsi_ascii_text = BeautifulSoup(jitsi_page)
      jitsi_links=jitsi_ascii_text.find_all('a', attrs={'href': re.compile('\\/macosx\\/jitsi-.*\\.dmg$')})
      FRCAlert('Starting installer download\n')
      jitsi_dmg=requests.get(jitsi_links[0]['href'])
      FRCAlert('Jitsi download complete\n')
      with open('jitsi-installer.dmg','wb') as f:
	for chunk in jitsi_dmg.iter_content(chunk_size=1024):
	  if chunk:
	    f.write(chunk)
	    f.flush()
      f.close()
      FRCAlert('Running installer\n')
      os.system(' open jitsi-installer.dmg')
    except Exception as e:
      printError(e)

# This function installs Thunderbird with Engimail	
def getThunderbirdWithEnigmail(lang):
    getThunderbird(lang)
    getEnigmail(enigmail_url)
    installEnigmail()
  
# This function downloads Cryptocat plugin
def downloadCryptoCat():
    try:
      FRCAlert('in CryptoCat downloading..\n')
      cat_page = requests.get(cryptocat_url ).content
      cat_ascii_text = BeautifulSoup(cat_page)
      cat_links=cat_ascii_text.find_all('a', attrs={'href': re.compile('\\/cryptocat-.*\\.xpi*')})[0]['href']
      FRCAlert('contents of cat_links: ' + str(cat_links) + '\n')
      cat_xpi=requests.get(cat_links)
      FRCAlert('cryptocat.xpi\n')
      FRCAlert('scraped and downloaded fake domain detective\n')
      f = open('cryptocat.xpi','wb')
      f.write(cat_xpi.content)
      f.close()
    except Exception as e:
      printError(e)
   
# This function installs Cryptocat plugin  
def installCryptoCat():
  installFirefoxPlugin('cryptocat.xpi')
  
# This function downloads and installs Cryptocat plugin  
def getCryptoCat():
  downloadCryptoCat()
  installCryptoCat()
  
# This function downloads and build Tails iso  
def getTailsISO():
  tails_ascii_text = BeautifulSoup(requests.get(tails_url).content)
  tails_iso_link = tails_ascii_text.find_all('a', attrs = {'href': re.compile('tails.*\\.iso$')})[0]['href']
  FRCAlert('Got Tails download link: ' + str(tails_iso_link))
  sig_link = tails_ascii_text.find_all('a', attrs = {'href': re.compile('tails.*\\.iso\\.sig$')})[0]['href']
  sig_file=requests.get(sig_link,stream=True)
  iso_file = requests.get(tails_iso_link,stream=True)
  FRCAlert("Downloading iso file..")
  with open("tails.iso","wb") as f:
    for chunk in iso_file.iter_content(chunk_size=1024):
      if chunk:
	f.write(chunk)
	f.flush()
  f.close()
  FRCAlert("Downloading signature file..")
  with open('tails.sig','wb') as f:
    for chunk in sig_file.iter_content(chunk_size=1024):
      if chunk:
	f.write(chunk)
	f.flush()
  f.close()
  try:
    gpg=gnupg.GPG()
    s=gpg.recv_keys('pool.sks-keyservers.net',tails_finger_print)
    f=open("tails.sig","rb")
    verified=gpg.verify_file(f,os.path.abspath("tails.iso"))
    if verified :
      FRCAlert("Signature verified..")
      os.open("hdiutil burn tails.iso")
      FRCAlert("Iso is burning now please wait..")
      f.close()
  except Exception as e:
      print e

# This function downloads FakeOut plugin  
def downloadFakeOut(url):
  try:
    FRCAlert('in getFakeDoamin\n')
    fake_page = requests.get(url).content
    fake_ascii_text = BeautifulSoup(fake_page)
    fake_links=fake_ascii_text.find_all('a', attrs={'href': re.compile('\\/fake_domain_detective-.*\\.xpi*')})[0]['href']
    FRCAlert('contents of fake_links: ' + str(fake_links) + '\n')
    fake_xpi=requests.get(fake_links)
    FRCAlert('FakeDomain.xpi\n')
    FRCAlert('scraped and downloaded fake domain detective\n')
    f = open('fake_domain_detective.xpi','wb')
    f.write(fake_xpi.content)
    f.close()
  except Exception as e:
    printError(e)

# This function installs FakeOut plugin
def installFakeOut():
  installFirefoxPlugin('fake_domain_detective.xpi')


# This function downloads and installs FakeOut plugin
def getFakeOut():
    downloadFakeOut(FakeDomain_url)
    installFakeOut()

