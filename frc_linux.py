#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Fly Rod Crosby: Making Cryptoparties Easier since 1897!
# All original material Copyright (C) 2013 Peter Bourgelais
# Original file from xpi2folders: xpi2folders.py Copyright 
# (C) 2011-2012, Kirill Kozlovskiy
# This program is free software. You can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free  Software Foundation; either version 2
# of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program, if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 
# 02111-1307, USA.

import os
import re
import sys
import requests
import hashlib
import urllib
import urllib2
import zipfile
import tarfile
import platform
import wx
from shutil import copyfile
from bs4 import BeautifulSoup
from urlparse import urlparse
from frc_linuxconfig import *
from xml.dom import minidom
from os.path import abspath, realpath, dirname, join as joinpath


resolved = lambda x: realpath(abspath(x))

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
    print path
    task="cp "+plugin_name+" "+ path+plugin_id+".xpi"
    os.system(task)

def FRCAlert(text):
    print text

def getGPG(GPGurl):
    try:	
        home = os.path.expanduser("~")
	if os.path.isdir(home+"/.gnupg") != True:
	    print "Gnupg is already installed :)"
            exit(0)
	else:
            # Getting the link to dowload:
	    page = requests.get(GPGurl,verify=True)
            soup = BeautifulSoup(page.content, "lxml")
            link = soup.find_all('a',attrs={'href':re.compile("gnupg-.*.tar.bz2$")})[0]['href']
	    siglink = soup.find_all('a',attrs={'href':re.compile("gnupg-.*.tar.bz2.sig$")})[0]['href']
            if len(link)==0 or len(siglink)==0 :
                print "Couldn't found gpg doxnload link. Please telle whoever is running the cryptoperty.\n"
            file_stream = requests.get('http://www.gnupg.org/'+link, stream=True)
            i=0 
            with open(gpg_file_name,'wb') as f:
                for chunk in file_stream.iter_content(chunk_size=1024):
                    if chunk:
                        i+=1
                        f.write(chunk)
                        f.flush()
                        print "Download done.."
                	os.system("tar xvjf " + gpg_file_name)
        	        os.system ("apt-get install libgpg-error-dev && \
                	            apt-get install libgcrypt11-dev && \
                        	    apt-get install libksba-dev && \
	                            apt-get install libassuan-dev ")
        	        os.system("./gnupg-2.0.22/configure")
              	        os.system("make gnupg-2.0.22/po/Makefile.in.in")
               		os.system("make gnupg-2.0.22/po/Makefile.in.in  install")
		
			cert_file=requests.get(hkps_cert_link,verify=False)

	                path_to_cert=home+"/.gnupg/sks-keyservers.netCA.pem"
	
        	        with open("path_to_cert","wb") as f:
                	     for chunk in cert_file.iter_content(chunk_size=1024):
                        	 if chunk:
                                     f.write(chunk)
                                     f.flush()
	                f.close()
        	        with open(home+"/.gnupg/gpg.conf","a") as r:
                	    r.write("keyserver hkps://hkps.pool.sks-keyservers.net\nkeyserver-options ca-cert-file="+path_to_cert)
                	r.close()
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
    
def getTOR(url,lang):	
    try:
        # Get and parse the HTML of the download page
        tor_page=requests.get(url)
        tor_soup = BeautifulSoup(tor_page.content, "lxml")
        tor_zip_link=''
        tor_sig_links=''
        print 'Scraping the Tor Project site for the relevant links\n'
        if platform.machine()=='x86_64':
		tor_zip_link=tor_soup.find_all('a', attrs={'href': re.compile('tor-browser-linux64-.*' + lang + '.*.tar.xz$')})[0]['href']
        	tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('tor-browser-linux64-.*' + lang + '\\.tar.xz\\.*asc$')})[0]['href']
	else:
		tor_zip_link=tor_soup.find_all('a', attrs={'href': re.compile('tor-browser-linux32-.*' + lang + '.*.tar.xz$')})[0]['href']
                tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('tor-browser-linux32-.*' + lang + '\\.tar.xz\\.*asc$')})[0]['href']
        tor_file_name=tor_zip_link[25:63]

	#We parse the url and add the scheme because the href text in the source looks something like this:
        # ../dist/torbrowser/3.5.2.1/torbrowser-install-3.5.2.1_vi.exe
        #Therefore we need to take the url in the href attribute, parse out the netloc, and add https to the beginning.
        tor_url_parsed=urlparse(url)
	tor_url_base=tor_url_parsed.scheme + '://' + tor_url_parsed.netloc
        
        #print unicode(tor_link_exes) + '\n\n' + unicode(tor_sig_links)
        #In an earlier version of the Tor download page, the stable version
        #and the beta version were available and localized to American English,
        #Hence the two for loops below to find the non-beta version.
        #TO-DO: Remove the for loops to make the code more readable.
        #for exe_link in tor_link_exes:
        # if len(exe_link) > 0 and 'beta' not in exe_link['href']:
        # tor_exe_link=tor_url_base+exe_link['href'][2:]
        # FRCAlert(tor_exe_link + '\n')

        #for sig_link in tor_sig_links:
        # if len(sig_link) > 0 and 'beta' not in sig_link['href']:
        # tor_sig_link=tor_url_base+sig_link['href'][2:]
        # FRCAlert(tor_sig_link + '\n')
        
        #Check to make sure we have an exe link and a signature link
        #to request.
        if len(tor_zip_link) == 0 or len(tor_sig_links) == 0:
            print "Couldn't find download link for Tor. Please tell whoever is running the Cryptoparty.\n"
            exit()
        #Download and write to file (see getGPG for an explanation of the with block below
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
	# And now to verify the executable.
        # I just hope that nobody tampered with both the exe AND the asc!
        # If they did, I'm going to download Erinn Clark's GPG off one of a list
        # of public key servers (from the Thunderbird defaults) and verify with
        # both keys. If either one fails, I'll throw an exception.
        # TO-DO: Tweak the key verification. It might be a good idea to use
        # a server that speaks HKPS if we can find one.
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
        
        
 
def installThunderbird():
    try:
	os.system("sudo apt-get install thunderbird")      
    except Exception as e:
        printError(unicode(e))

def getEnigmail(url):
    try:
        enigmail_page = requests.get(url).content
        enigmail_soup = BeautifulSoup(enigmail_page, "lxml")
        enigmail_links=enigmail_soup.find_all('a', attrs={'href': re.compile('enigmail.*sm\\+tb\\.xpi')})[:2]
        enigmail_xpi=requests.get(enigmail_links[0]['href'])
        FRCAlert('Downloaded enigmail.xpi\n')
        enigmail_asc=requests.get(HTTPSthis(enigmail_links[1]['href']))
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

def getTorBirdy():
    try:
        torbirdy_xpi=requests.get(torbirdy_xpi_url)
        FRCAlert('Downloaded torbirdy.xpi\n')
        torbirdy_asc=requests.get(torbirdy_xpi_sig_url)
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

def installEnigmail():
    try:
	os.system("sudo apt-get install enigmail")
    except Exception as e:
    	printError(unicode(e))

def installTorBirdy():
    try:
      installPlugin("torbirdy.xpi")
    except Exception as e:
      printError(unicode(e))

def getJitsi():
    try:
	os.system("sudo apt-get install jitsi")
    except Exception as e:
        print e
	
def getThunderbirdWithEnigmail():
	installThunderbird()
	installEnigmail()
  
def downloadCryptoCat():
    try:
      FRCAlert('In CryptoCat downloading..\n')
      cat_page = requests.get(cryptocat_url ).content
      cat_soup = BeautifulSoup(cat_page, "lxml")
      cat_links=cat_soup.find_all('a', attrs={'href': re.compile('\\/cryptocat-.*\\.xpi*')})[0]['href']
      cat_xpi=requests.get(cat_links)
      FRCAlert('scraped and downloaded fake domain detective\n')
      f = open('cryptocat.xpi','wb')
      f.write(cat_xpi.content)
      f.close()
    except Exception as e:
      printError(e)
      
def installCryptoCat():
    installFirefoxPlugin('cryptocat.xpi')
  
def getCryptoCat():
  downloadCryptoCat()
  installCryptoCat()

#[5]Big HTTPS download, but there is a signature over HTTP
def getTailsISO():
  global home
  tails_soup = BeautifulSoup(requests.get(tails_url).content, "lxml")
  tails_iso_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso$')})[0]['href']
  FRCAlert('Got Tails download link: ' + str(tails_iso_link))
  sig_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso\\.sig$')})[0]['href']
  sig_file=requests.get(sig_link,stream=True)
  iso_file = requests.get(tails_iso_link,stream=True)
  FRCAlert("Downloading iso file..")
  with open(home+'/tails.iso','wb') as f:
      for chunk in iso_file.iter_content(chunk_size=1024):
          if chunk:
	      f.write(chunk)
	      f.flush()
  f.close()
  FRCAlert("Downloading signature file..")
  with open(home+'/tails.sig','wb') as f:
    for chunk in sig_file.iter_content(chunk_size=1024):
      if chunk:
	f.write(chunk)
	f.flush()
  f.close()    
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

def downloadFakeOut(url):
  try:
    FRCAlert('in getFakeDoamin\n')
    fake_page = requests.get(url).content
    fake_soup = BeautifulSoup(fake_page, "lxml")
    fake_links=fake_soup.find_all('a', attrs={'href': re.compile('\\/fake_domain_detective-.*\\.xpi*')})[0]['href']
    FRCAlert('contents of fake_links: ' + str(fake_links) + '\n')
    fake_xpi=requests.get(fake_links)
    FRCAlert('FakeDomain.xpi\n')
    #fake_asc=requests.get(HTTPSthis(fake_links))
    FRCAlert('scraped and downloaded fake domain detective\n')
    f = open('fake_domain_detective.xpi','wb')
    f.write(fake_xpi.content)
    f.close()
  except Exception as e:
    printError(e)

def installFakeOut():
    installFirefoxPlugin('fake_domain_detective.xpi')

def getFakeOut():
    downloadFakeOut(FakeDomain_url)
    installFakeOut()

def downloadFakeOut(url):
  try:
    FRCAlert('In getFakeDoamin\n')
    fake_page = requests.get(url).content
    fake_soup = BeautifulSoup(fake_page, "lxml")
    fake_links=fake_soup.find_all('a', attrs={'href': re.compile('\\/fake_domain_detective-.*\\.xpi*')})[0]['href']
    fake_xpi=requests.get(fake_links)
    FRCAlert('FakeDomain.xpi\n')
    FRCAlert('scraped and downloaded fake domain detective\n')
    f = open('fake_domain_detective.xpi','wb')
    f.write(fake_xpi.content)
    f.close()
  except Exception as e:
    printError(e)

def installFakeOut():
  installFirefoxPlugin('fake_domain_detective.xpi')

def getFakeOut():
    downloadFakeOut(FakeDomain_url)
    installFakeOut()
