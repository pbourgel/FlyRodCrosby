import os

gpg4win_url = u'http://www.gpg4win.org/download.html'
tor_url = u'https://www.torproject.org/projects/torbrowser.html.en#Download-torbrowserbundle'
jitsi_url = u'https://jitsi.org/Main/Download'
#SOMEONE PLEASE CHECK THAT I GOT ERINN CLARK'S GPG INFO RIGHT
#tor_dev_gpg_fingerprint = '8738A680B84B3031A630F2DB416F061063FEE659'
tor_dev_gpg_id = u'63FEE659'
tor_dev_gpg_name = u'Erinn Clark (erinn@torproject.org)'
enigmail_dev_gpg_id = u'9369CDF3'
gpg_servers = ['pool.sks-keyservers.net','subkeys.pgp.net','sks.mit.edu']
#TO-DO: We need to substitute whatever the language variable needs to be in here
cryptocat_url = u'https://addons.mozilla.org/en-US/firefox/addon/cryptocat/'
enigmail_url = u'https://www.enigmail.net/download/download-static.php'
thunderbird_url = u'https://www.mozilla.org/en-US/thunderbird/all.html'

jitsi_url = u'https://jitsi.org/Main/Download'

try:
    os.environ['PROGRAMFILES(X86)']
    arch=64
except KeyError:
    arch=32

if arch == 64:
    thunderbird_ext_dir = 'C:\\Program Files (x86)\\Mozilla Thunderbird\\extensions\\'
    thunderbird_main_dir = r'""C:\Program Files (x86)\Mozilla Thunderbird\thunderbird.exe""'
    gpg4win_path = 'C:\\Program\ Files\ (x86)\\GNU\\GnuPG\\gpg2.exe'
    tbird_reg_str = r'SOFTWARE\Wow6432Node\Mozilla\Mozilla Thunderbird\Extensions'
else:
    thunderbird_ext_dir = 'C:\\Program Files\\Mozilla Thunderbird\\extensions\\'
    thunderbird_main_dir = r'""C:\Program Files\Mozilla Thunderbird\thunderbird.exe""'
    gpgrwin_path = 'C:\\Program\ Files\\GNU\\GnuPG\\gpg2.exe'
    tbird_reg_str = r'SOFTWARE\Mozilla\Mozilla Thunderbird\Extensions'


