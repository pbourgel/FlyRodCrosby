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
from xml.dom import minidom
import urllib2,urllib

import wx


def install_Firefox_plugin(plugin_name):
  task="unzip -p "+plugin_name+" install.rdf > install.rdf"
  print task 
  os.system(task) #" unzip -p enigmail.xpi install.rdf >   install.rdf"
  xmldoc = minidom.parse("install.rdf")
  dom = minidom.parseString(xmldoc.toxml())
  plugin_id = str(dom.getElementsByTagName("em:id")[0].toxml().replace('<em:id>','').replace('</em:id>',''))
  print plugin_id
  
  #profile=os.listdir("./.icedove")[0]

  for x in os.listdir("./Library/Application Support/Firefox/"):
	  if x.endswith(".default"):
		  profile=x

  path="./Library/Application Support/Firefox/"+profile+"/extensions/" 
  print path
  path=path +plugin_id+"/"
  task1="mkdir "+path
  print task1
  os.system(task1)
  task2="unzip "+plugin_name +" -d "+path

  os.system(task2)



def install_plugin(plugin_name):
  task="unzip -p "+plugin_name+" install.rdf > install.rdf"
  os.system(task) #" unzip -p enigmail.xpi install.rdf >   install.rdf"
  xmldoc = minidom.parse("install.rdf")
  dom = minidom.parseString(xmldoc.toxml())
  plugin_id = str(dom.getElementsByTagName("em:id")[0].toxml().replace('<em:id>','').replace('</em:id>',''))
  print plugin_id

  #profile=os.listdir("./.thunderbird")[0]

  for x in os.listdir("./.thunderbird"):
	  if x.endswith(".default"):
		  profile=x
  #/Library/Thunderbird/Profiles/
  path="./Library/Thunderbird/"+profile+"/extensions/" #don hesitate to change thunderbird to icedove
  #print path
  path=path +plugin_id+"/"
  task1="mkdir "+path
  print task1
  os.system(task1)
  task2="unzip "+plugin_name+" -d "+path

  os.system(task2)
  

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
  page = requests.get(url,verify=False)
  soup = BeautifulSoup(page.content)
  link=soup.find_all('a',attrs={'href': re.compile("GPG%20Suite *")}) [0]['href'] 

  #link = url  + link
  print link
  macGPG_file=requests.get(link,stream=True,verify=False)
  with open('GPG_Suite_2013.dmg','wb') as f:
   print "The GPG Suite Tools is downloading..\n"
   for chunk in macGPG_file.iter_content(chunk_size=1024):
     if chunk:
       f.write(chunk)
       f.flush
   f.close()
  os.system("open GPG_Suite_2013.dmg")
    #gpg_page=requests.get(url)
    #gpg4win_soup = BeautifulSoup(gpg_page.content)
    #gpg4win_link=gpg4win_soup.find_all('a', attrs={'href': re.compile('gpg4win-vanilla.*exe$')})[0]['href']
    #gpg4win_checksums=gpg4win_soup.find_all('code')
    #gpg4win_file=requests.get(gpg4win_link,stream=True) 
    #with open('gpg4win.exe','wb') as f:
        #for chunk in gpg4win_file.iter_content(chunk_size=1024): 
            #if chunk: # filter out keep-alive new chunks
                #f.write(chunk)
                #f.flush()
	#f.close()
    #FRCAlert("Calculating and verifying SHA1, which is geek speak for making sure that nobody changed the file during download.\n")
    #sha1 = hashlib.sha1()
    #f = open('gpg4win.exe','rb')
    #try:
        #sha1.update(f.read())
    #finally:
        #f.close()
    #gpg4win_hash = sha1.hexdigest()
    #checksum_verified=False
    #for checksum in gpg4win_checksums:
        #if gpg4win_hash in checksum:
            #FRCAlert("SHA1 verified, running installer\n")
            #checksum_verified=True
            #os.system("gpg4win.exe")
    #if checksum_verified == False:
        #FRCAlert("SHA1 verification failed!  Hide yo kids!  Hide yo wife!  They messin' with everybody out here!\n")
    




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
ddef getTOR(url, lang):	
    try:
        #get and parse the HTML of the download page
        tor_page=requests.get(url)
        tor_soup = BeautifulSoup(tor_page.content)
        tor_zip_link=''
        tor_sig_links=''
        FRCAlert('Scraping the Tor Project site for the relevant links\n')
        #Find the anchor tags for the language's EXE and OpenPGP signature
        tor_zip_link=tor_soup.find_all('a', attrs={'href': re.compile('TorBrowserBundle-.*' + lang + '.*.zip$')})[0]['href']
        tor_sig_links=tor_soup.find_all('a', attrs={'href': re.compile('TorBrowserBundle-.*' + lang + '\\.zip\\.*asc$')})[0]['href']
        print tor_zip_link
        print tor_sig_links
        
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
        #for exe_link in tor_link_exes:
        #    if len(exe_link) > 0 and 'beta' not in exe_link['href']:
        #        tor_exe_link=tor_url_base+exe_link['href'][2:]
        #        FRCAlert(tor_exe_link + '\n')

        #for sig_link in tor_sig_links:
        #    if len(sig_link) > 0 and 'beta' not in sig_link['href']:
        #        tor_sig_link=tor_url_base+sig_link['href'][2:]
        #        FRCAlert(tor_sig_link + '\n')
        
        #Check to make sure we have an exe link and a signature link
        #to request.
        if len(tor_zip_link) == 0 or len(tor_sig_links) == 0:
            FRCAlert("Couldn't find download link for Tor.  Please tell whoever is running the Cryptoparty.\n")
            exit()
        FRCAlert('Found download links.  Downloading the zip from ' + tor_zip_link + '\n')
        #Download and write to file (see getGPG for an explanation of the with block below
        
        tor_zip_link='https://www.torproject.org'+tor_zip_link[2:]
        
        #tor_zip_link='https://www.torproject.org/dist/torbrowser/3.5.2.1/TorBrowserBundle-3.5.2.1-osx32_en-US.zip'
        tor_zip_file=requests.get(tor_zip_link,stream=True) 
        
        with open('tor.zip','wb') as f:
            for chunk in tor_zip_file.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        tor_sig_links='https://www.torproject.org'+tor_sig_links[2:]
        FRCAlert('Downloaded zip.  Now downloading GPG signature from ' + tor_sig_links + '\n')
        #Now download the signature
        tor_sig_file=requests.get(tor_sig_links)
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
            gpg.recv_keys('pool.sks-keyservers.net',tor_dev_gpg_fingerprint)
            f = open('tor_sig.asc','rb')
            #g = open('tor.exe','rb')
            FRCAlert('Verifying exe with GPG key in keyring\n')
            verified_with_asc = gpg.verify_file(f,os.path.abspath('tor.zip'))
            if verified_with_asc:
                FRCAlert("The Tor executable checks out.  Let's extract it.\n")
                os.system(' open tor.zip')
                f.close()
                #g.close()
                task="open TorBrowserBundle_"+lang 
                os.system( task )
            else:
                FRCAlert("EXE verification failed.  Please tell whoever is running your Cryptoparty." + "\n")
                f.close()
                #g.close()
                exit()
        except Exception as e:
            FRCAlert('Problem downloading Tor: Please show this to your facilitator: ' + unicode(e) + '\n')
    except Exception as e:
        #printError(unicode(e))
 
def getThunderbird(lang):
    try:
        tbird_soup=BeautifulSoup(requests.get(thunderbird_url).content)#here we go very fast :p
        tbird_link=tbird_soup.find_all('a',attrs={'href': re.compile('.*os=osx.*lang=' + lang)})
        print tbird_link
        tbird_file=requests.get(tbird_link[0]['href'],stream=True)
        #Grease is the word...
        with open('thunderbird-installer.dmg','wb') as f:
            for chunk in tbird_file.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        f.close()
        #I WOULD add signature verification code here, BUT THERE'S NO FUCKING
        #PGP key!
        #yeah soon ;)
        os.system('open thunderbird-isntaller.dmg')
    except Exception as e:
        printError(unicode(e))

def getEnigmail(url):
    try:
	RCAlert('in getEnigmail\n')
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
            FRCAlert("The Enigmail plugin checks out. Let's install it in Thunderbird\n")
            x.close()
        else:
            FRCAlert("Enigmail verification failed. Please tell whoever is running your Cryptoparty.\n")
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

def installEnigmail():
    try:
      install_plugin("enigmail.xpi")
        #FRCAlert('Determined Thunderbird extensions directory: ' + thunderbird_ext_dir + '\n')
        #FRCAlert('Determined Thunderbird main directory: ' + thunderbird_main_dir + '\n')
        #copyfile(os.getcwd() + '\\' + 'enigmail.xpi', thunderbird_ext_dir + 'enigmail.xpi')
        #xpi_id = processXpi(thunderbird_ext_dir + 'enigmail.xpi', thunderbird_ext_dir)['id']
        #FRCAlert('Modifying registry\n')
        #with CreateKey(HKEY_LOCAL_MACHINE,tbird_reg_str) as key:
            #SetValueEx(key,"{3550f703-e582-4d05-9a08-453d09bdfdc6}",0,REG_SZ,xpi_id)
            #FRCAlert('Set key in registry\n')
            #CloseKey(key)
        #FRCAlert('Starting Thunderbird\n')
        #if start_after_copied:
            #os.system(thunderbird_main_dir)
    except Exception as e:
        printError(unicode(e))

def installTorBirdy():
    try:
      install_plugin("torbirdy.xpi")
        #FRCAlert('Determined Thunderbird extensions directory: ' + thunderbird_ext_dir + '\n')
        #FRCAlert('Determined Thunderbird main directory: ' + thunderbird_main_dir + '\n')
        #copyfile(os.getcwd() + '\\' + 'torbirdy.xpi', thunderbird_ext_dir + 'torbirdy.xpi')
        #xpi_id = processXpi(thunderbird_ext_dir + 'torbirdy.xpi', thunderbird_ext_dir)['id']
        #FRCAlert('Modifying registry\n')
        #with CreateKey(HKEY_LOCAL_MACHINE,tbird_reg_str) as key:
           #SetValueEx(key,"{3550f703-e582-4d05-9a08-453d09bdfdc6}",0,REG_SZ,xpi_id)
           #FRCAlert('Set key in registry\n')
           #CloseKey(key)
        #FRCAlert('Starting Thunderbird\n')
        #os.system(thunderbird_main_dir)
    except Exception as e:
        printError(unicode(e))


def getJitsi(url):
    try:
         FRCAlert('In getJitsi\n')
      jitsi_page = requests.get(url).content
      jitsi_soup = BeautifulSoup(jitsi_page)
      jitsi_links=jitsi_soup.find_all('a', attrs={'href': re.compile('\\/macosx\\/jitsi-.*\\.dmg$')})
      print jitsi_links
      FRCAlert('Starting installer download\n')
      jitsi_dmg=requests.get(jitsi_links[0]['href'])
      FRCAlert('Jitsi download complete\n')
      with open('jitsi-installer.dmg','wb') as f:
	for chunk in jitsi_dmg.iter_content(chunk_size=1024):
	  if chunk: # filter out keep-alive new chunks
	    f.write(chunk)
	    f.flush()
	f.close()
	#I WOULD put GPG signature verification code here, but SOMEBODY didn't add a .asc!
	FRCAlert('Running installer\n')
	os.system(' open jitsi-installer.dmg')
    except Exception as e:
        printError(e)
	
def getThunderbirdWithEnigmail(lang, start_after_copied):
    getThunderbird(lang)
    getEnigmail(enigmail_url)
    installEnigmail()

#[2/3]What's a good browser decision here?  Should I just install Firefox if it isn't installed, or add it to the TBB?
def getCryptoCat():
    pass

#[1]Straight HTTP download.  Does offer a sha256 sum over HTTP.
#def getBleachBit():#We can think about another alternative.. 
    #try:
        #bleachbit_soup = BeautifulSoup(requests.get(bleachbit_url).content)
        #bleachbit_exe_link = bleachbit_soup.find_all('a', attrs = {'href': re.compile('BleachBit-.*\\.exe$')})[0]['href']
        #FRCAlert('Found download links: ' + str(bleachbit_exe_link))
        #bleachbit_exe = requests.get(bleachbit_base_url + bleachbit_exe_link)
        #with open('bleachbit-installer.exe','wb') as f:
            #for chunk in bleachbit_exe.iter_content(chunk_size=1024): 
                #if chunk: # filter out keep-alive new chunks
                    #f.write(chunk)
                    #f.flush()
        #f.close()
        #FRCAlert('Bleachbit EXE written to disk.  Running installer.')
        #os.system('bleachbit-installer.exe')
    #except Exception as e:
        #printError(e)
    

#[4]Weird POST and transient URL stuff here, HTTP but there is PGP sig
def getTrueCrypt():
    FRCAlert('TrueCrypt download stub here.')
    #url_trueCrypt = "http://www.truecrypt.org/dl"
    req = urllib2.Request(url_trueCrypt)  
    values = {"DownloadVersion" : "7.1a", "MacOSXDownload" : "Download"}
    data = urllib.urlencode(values)
    response = urllib2.urlopen(req, data)
    open("truecrypt.dmg","w").write(response.read())
    os.system("open truecrypt.dmg ")

#[5]Big HTTPS download, but there is a signature over HTTP
def getTailsISO():
    tails_soup = BeautifulSoup(requests.get(tails_url).content)
    tails_iso_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso$')})[0]['href']
    FRCAlert('Got Tails download link: ' + str(tails_iso_link))
    sig_link = tails_soup.find_all('a', attrs = {'href': re.compile('tails.*\\.iso\\.sig$')})[0]['href']
    #sig_link='https://tails.boum.org/torrents/files/tails-i386-0.22.1.iso.sig'
    sig_file=requests.get(sig_link,stream=True)
    iso_file = requests.get(tails_iso_link,stream=True)
    #Downloading iso file 
    FRCAlert("Downloading iso file..")
    with open("tails.iso","wbe") as f:
      for chunk in iso_file.iter_content(chunk_size=1024):
	if chunk:
	  f.write(chunk)
	  f.flush()
    f.close()
    #downloading signature file
    FRCAlert("Downloading signature file..")
    with open('tails.sig','wb') as f:
      for chunk in sig_file.iter_content(chunk_size=1024):
	if chunk:
	  f.write(chunk)
	  f.flush()
    f.close()
    
  try:
    gpg=gnupg.GPG()
    s=gpg.recv_keys('pool.sks-keyservers.net',tails_finger_print) #tails_finger_print
    #print s
    f=open("tails.sig","rb")
    verified=gpg.verify_file(f,os.path.abspath("tails.iso"))
    if verified :
      FRCAlert("Signature verified..")
      os.open("hdiutil burn tails.iso") #osx command line
      FRCAlert("Iso is burning now please wait..")
    f.close()
  except Exception as e:
  print e

def downloadFakeOut():
    try:
      FRCAlert('in getFakeDoamin\n')
      fake_page = requests.get(url).content
      fake_soup = BeautifulSoup(fake_page)
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
  install_plugin('fake_domain_detective.xpi')
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

erbird\n')
#        os.system(thunderbird_main_dir)
#    except Exception as e:
#        printError(unicode(e))

#[2/3]HTTPS download, PGP signature coming soon
def getFakeOut():
    downloadFakeOut()
    installFakeOut()

tallFakeOut()

)

tallFakeOut()

)

tallFakeOut()

f getFakeOut():
    downloadFakeOut()
    installFakeOut()

tallFakeOut()

)

tallFakeOut()

)

tallFakeOut()

()

