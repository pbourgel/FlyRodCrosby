#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc_linux.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the functions that used to download,
#                   verify and install the different tools.
#################################################################################


import os
import re
import requests
import platform
import wx
from bs4 import BeautifulSoup
from urlparse import urlparse
from frc_linuxconfig import *
from xml.dom import minidom
from os.path import abspath, realpath, dirname, join as joinpath


# This function installs the given plugin into Firefox
def installFirefoxPlugin(plugin_name):
    task="unzip -p "+plugin_name+" install.rdf > install.rdf"
    os.system("rm -rf install.rdf")
    os.system(task)
    xmldoc = minidom.parse("install.rdf")
    dom = minidom.parseString(xmldoc.toxml())
    plugin_id = str(dom.getElementsByTagName("em:id")[0].toxml().replace('<em:id>','').replace('</em:id>','')) 
    for x in os.listdir(os.path.expanduser("~")+"/.mozilla/firefox/"):
        if x.endswith(".default"):
            profile=x
            break
    path=os.path.expanduser("~")+"/.mozilla/firefox/"+profile+"/extensions/"+plugin_id+".xpi"
    plugin_exists=os.path.isfile(path)
    if plugin_exists:
        FRCAlert(plugin_name[:-4]+" is already installed..")
        return 
    task="cp "+plugin_name+" "+ path
    os.system(task)

# This function installs the given plugin into Thunderbird
def installPlugin(plugin_name):
    task="unzip -p "+plugin_name+" install.rdf > install.rdf"
    os.system("rm install.rdf")
    os.system(task)
    xmldoc = minidom.parse("install.rdf")
    dom = minidom.parseString(xmldoc.toxml())
    plugin_id = str(dom.getElementsByTagName("em:id")[0].toxml().replace('<em:id>','').replace('</em:id>',''))
    for x in os.listdir(".thunderbird/"):
        if x.endswith(".default"):
                profile=x
                break
    path=".thunderbird/"+profile+"/extensions/"
    task="cp "+plugin_name+" "+ path+plugin_id+".xpi"
    os.system(task)

def FRCAlert(text):
    print text

# This function downloads and installs GPG program
def getGPG(GPGurl):
    try:	
        home = os.path.expanduser("~")
	if os.path.isdir(home+"/.gnupg") == True:
	    print "Gnupg is already installed :)"
            exit(0)
	else:
            # Getting the link to dowload:
	    page = requests.get(GPGurl,verify=True)
            ascii_text = BeautifulSoup(page.content, "lxml")
            link = ascii_text.find_all('a',attrs={'href':re.compile("gnupg-.*.tar.bz2$")})[0]['href']
	    siglink = ascii_text.find_all('a',attrs={'href':re.compile("gnupg-.*.tar.bz2.sig$")})[0]['href']
            if len(link)==0 or len(siglink)==0 :
                print "Couldn't found gpg doxnload link. Please tell whoever is running the cryptoperty.\n"
            file_stream = requests.get('http://www.gnupg.org/'+link, stream=True)
            with open(gpg_file_name,'wb') as f:
                for chunk in file_stream.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print "Download done.."
            os.system("mkdir gnupg; tar xvjf " + gpg_file_name + " -C gnupg --strip-components 1")
            os.system ("apt-get install -y libgpg-error-dev libgcrypt11-dev libksba-dev libassuan-dev")
            os.system("cd gnupg; ./configure && make && make install")
            cert_file=requests.get(hkps_cert_link,verify=False)
            path_to_cert=home+"/.gnupg/sks-keyservers.netCA.pem"
            with open("path_to_cert","wb") as f:
                for chunk in cert_file.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
	    with open(home+"/.gnupg/gpg.conf","a") as f:
                f.write("keyserver hkps://hkps.pool.sks-keyservers.net\nkeyserver-options ca-cert-file="+path_to_cert)
    except Exception as e:
        print "Error while downloading GnuPG: Please show this to your facilitator ERROR:", e
    
try:
    import gnupg
    gpg=gnupg.GPG()
except Exception:
    FRCAlert("GnuPG not found.  Downloading it now.\n")
    FRCAlert("Expect an installer window in 5 minutes.\n")
    getGPG(macGPGurl)
    import gnupg


def httpsThis(url):
    return re.sub(pattern='http', repl='https', string=url)

def printError(text):
    print 'An error occured with your download.  Please show this to your Cryptoparty facilitator: ' + str(text)
    print "ERROR: "+ str(text)

# This function downloads and installs the Tor browser bundle    
def getTOR(url,lang):	
    try:
        # Get and parse the HTML of the download page
        tor_page=requests.get(url)
        tor_ascii_text = BeautifulSoup(tor_page.content, "lxml")
        tor_zip_link=''
        tor_sig_links=''
        print 'Scraping the Tor Project site for the relevant links\n'
        if platform.machine()=='x86_64':
		tor_zip_link=tor_ascii_text.find_all('a', attrs={'href': re.compile('tor-browser-linux64-.*' + lang + '.*.tar.xz$')})[0]['href']
        	tor_sig_links=tor_ascii_text.find_all('a', attrs={'href': re.compile('tor-browser-linux64-.*' + lang + '\\.tar.xz\\.*asc$')})[0]['href']
	else:
		tor_zip_link=tor_ascii_text.find_all('a', attrs={'href': re.compile('tor-browser-linux32-.*' + lang + '.*.tar.xz$')})[0]['href']
                tor_sig_links=tor_ascii_text.find_all('a', attrs={'href': re.compile('tor-browser-linux32-.*' + lang + '\\.tar.xz\\.*asc$')})[0]['href']
        tor_file_name=tor_zip_link[25:63]
	tor_url_parsed=urlparse(url)
	tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc        
        # Check to make sure we have an exe link and a signature link
        # to request.
        if len(tor_zip_link) == 0 or len(tor_sig_links) == 0:
            print "Couldn't find download link for Tor. Please tell whoever is running the Cryptoparty.\n"
            exit()
        tor_zip_link='https://www.torproject.org'+tor_zip_link[2:]
        tor_zip_file=requests.get(tor_zip_link,stream=True)
       	with open(tor_file_name,'wb') as f:
            for chunk in tor_zip_file.iter_content(chunk_size=1024):
                if chunk:
		    f.write(chunk)
                    f.flush()
        tor_sig_links='https://www.torproject.org'+tor_sig_links[2:]
        # Now download the signature
        tor_sig_file=requests.get(tor_sig_links)
        f=open(tor_file_name+'.asc', 'wb')
        f.write(tor_sig_file.content)
        f.close()
	try:
            gpg=gnupg.GPG(homedir="/tmp/gpg")
            gpg._create_trustdb()
            print 'Trying to download Tor devs GPG key\n'
            #TO-DO: Iterate through the standard servers in case sks-skyservers
            #is down.
            verified_with_asc = gpg.verify_file(open(tor_file_name), tor_file_name+'.asc')
            if verified_with_asc:
		task = "tar -xvJf "+tor_file_name
		os.system(task)
		os.system("tor-browser_en-US/Browser/start-tor-browser")
            else:
                print "EXE verification failed. Please tell whoever is running your Cryptoparty." + "\n"
        except Exception as e:
            print 'Problem downloading Tor: Please show this to your facilitator: ' + unicode(e) + '\n'
    except Exception as e:
        print unicode(e)
        
# This function installs Thunderbird        
def installThunderbird():
    try:
	os.system("sudo apt-get install thunderbird")      
    except Exception as e:
        printError(unicode(e))

# This function Downloads Engimail plugin
def getEnigmail(url):
    try:
        enigmail_page = requests.get(url).content
        enigmail_ascii_text = BeautifulSoup(enigmail_page, "lxml")
        enigmail_links=enigmail_ascii_text.find_all('a', attrs={'href': re.compile('enigmail.*sm\\+tb\\.xpi')})[:2]
        enigmail_xpi=requests.get(enigmail_links[0]['href'])
        FRCAlert('Downloaded enigmail.xpi\n')
        enigmail_asc=requests.get(HTTPSthis(enigmail_links[1]['href']))
        f = open('enigmail.xpi','wb')
        f.write(enigmail_xpi.content)
        f.close()
        f = open('enigmail.xpi.asc','wb')
        f.write(enigmail_asc.content)
        f.close()
        gpg=gnupg.GPG()
	#TO-DO: Iterate through the standard servers in case sks-skyservers
        #is down.
        gpg.recv_keys('pool.sks-keyservers.net',enigmail_dev_gpg_fingerprint)
        fd = open('enigmail.xpi.asc','rb')
        verified = gpg.verify_file(fd,os.path.abspath('enigmail.xpi'))
        if verified:
            FRCAlert("The Enigmail plugin checks out. Let's install it in Thunderbird\n")
            fd.close()
        else:
            FRCAlert("Enigmail verification failed. Please tell whoever is running your Cryptoparty.\n")
            fd.close()
            exit()	
    except Exception as e:
        printError(unicode(e))

# This function Downloads Torbirdy plugin
def getTorBirdy():
    try:
        torbirdy_xpi=requests.get(torbirdy_xpi_url)
        FRCAlert('Downloaded torbirdy.xpi\n')
        torbirdy_asc=requests.get(torbirdy_xpi_sig_url)
        f = open('torbirdy.xpi','wb')
        f.write(torbirdy_xpi.content)
        f.close()
        f = open('torbirdy.xpi.asc','wb')
        f.write(torbirdy_asc.content)
        f.close()
        gpg=gnupg.GPG()    
	#TO-DO: Iterate through the standard servers in case sks-skyservers
        #is down.
        gpg.recv_keys('pool.sks-keyservers.net',torbirdy_dev_gpg_fingerprint)
        fd = open('torbirdy.xpi.asc','rb')
        verified = gpg.verify_file(fd,os.path.abspath('torbirdy.xpi'))
        if verified:
            FRCAlert("The Torbirdy plugin checks out.  Let's install it in Thunderbird\n")
            fd.close()
        else:
            FRCAlert("Torbirdy verification failed.  Please tell whoever is running your Cryptoparty.\n")
            fd.close()
            exit()
    except Exception as e:
        printError(unicode(e))

# This function installs Engimail plugin
def installEnigmail():
    try:
	os.system("sudo apt-get install enigmail")
    except Exception as e:
    	printError(unicode(e))

# This function installs Torbirdy plugin
def installTorBirdy():
    try:
      installPlugin("torbirdy.xpi")
    except Exception as e:
      printError(unicode(e))

# This function installs Jitsi
def getJitsi():
    try:
	os.system("sudo apt-get install jitsi")
    except Exception as e:
        print e

# This function installs Thunderbird with Engimail
def getThunderbirdWithEnigmail():
	installThunderbird()
	installEnigmail()

# This function downloads Cryptocat plugin    
def downloadCryptoCat():
    try:
      FRCAlert('In CryptoCat downloading..\n')
      cat_page = requests.get(cryptocat_url ).content
      cat_ascii_text = BeautifulSoup(cat_page, "lxml")
      cat_links=cat_ascii_text.find_all('a', attrs={'href': re.compile('\\/cryptocat-.*\\.xpi*')})[0]['href']
      cat_xpi=requests.get(cat_links)
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
  global home
  tails_ascii_text = BeautifulSoup(requests.get(tails_url).content, "lxml")
  tails_iso_link = tails_ascii_text.find_all('a', attrs = {'href': re.compile('tails.*\\.iso$')})[0]['href']
  FRCAlert('Got Tails download link: ' + str(tails_iso_link))
  sig_link = tails_ascii_text.find_all('a', attrs = {'href': re.compile('tails.*\\.iso\\.sig$')})[0]['href']
  sig_file=requests.get(sig_link,stream=True)
  iso_file = requests.get(tails_iso_link,stream=True)
  FRCAlert("Downloading iso file..")
  with open(home+'/tails.iso','wb') as f:
      for chunk in iso_file.iter_content(chunk_size=1024):
          if chunk:
	      f.write(chunk)
	      f.flush()
  FRCAlert("Downloading signature file..")
  with open(home+'/tails.sig','wb') as f:
    for chunk in sig_file.iter_content(chunk_size=1024):
      if chunk:
	f.write(chunk)
	f.flush()
  try:
      gpg=gnupg.GPG()
      s=gpg.recv_keys('pool.sks-keyservers.net',tails_finger_print) #tails_finger_print
      f=open("tails.sig","rb")
      verified=gpg.verify_file(f,os.path.abspath(home+'/tails.iso'))
      if verified :
          FRCAlert("Signature verified..")
          os.system("growisofs -Z /dev/sr0="+home+"/tails.iso") #linux command line using growisofs
          FRCAlert("Live tails is ready")
      f.close()
  except Exception as e:
      print e

# This function downloads FakeOut plugin  
def downloadFakeOut(url):
  try:
    FRCAlert('in getFakeDoamin\n')
    fake_page = requests.get(url).content
    fake_ascii_text = BeautifulSoup(fake_page, "lxml")
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
