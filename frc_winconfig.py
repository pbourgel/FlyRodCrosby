# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc_winconfig.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the tools links and pgp keys information.
#####################################################################################

import os

# Define download urls and signature urls
gpg4win_url = u'http://www.gpg4win.org/download.html'
tor_url = u'https://www.torproject.org/projects/torbrowser.html.en#Download-torbrowserbundle'
jitsi_url = u'https://jitsi.org/Main/Download'
tor_dev_gpg_fingerprint = '8738A680B84B3031A630F2DB416F061063FEE659'
tor_dev_gpg_name = u'Erinn Clark (erinn@torproject.org)'
enigmail_dev_gpg_fingerprint = u'10B2E4A0E718BB1B2791DAC4F040E41B9369CDF3'
gpg_servers = ['pool.sks-keyservers.net','subkeys.pgp.net','sks.mit.edu','pgp.mit.edu']

# TO-DO: We need to substitute whatever the language variable needs to be in here
cryptocat_url = u'https://addons.mozilla.org/en-US/firefox/addon/cryptocat/'
enigmail_url = u'https://www.enigmail.net/download/download-static.php'
thunderbird_url = u'https://www.mozilla.org/en-US/thunderbird/all.html'
bleachbit_url = u'http://bleachbit.sourceforge.net/download/windows'
bleachbit_base_url = u'http://bleachbit.sourceforge.net/download/'
tails_url = u'http://bleachbit.sourceforge.net/download/windows'
torbirdy_xpi_url = u'https://www.torproject.org/dist/torbirdy/torbirdy-current.xpi'
torbirdy_xpi_sig_url = u'https://www.torproject.org/dist/torbirdy/torbirdy-current.xpi.asc'

# You can find this key by searching for "Jacob Appelbaum (offline long term identity key)"
torbirdy_dev_gpg_fingerprint = u'228FAD203DE9AE7D84E25265CF9A6F914193A197'
jitsi_url = u'https://jitsi.org/Main/Download'

# Are we on a 32-bit system or 64-bit?
try:
    os.environ['PROGRAMFILES(X86)']
    arch=64
except KeyError:
    arch=32

# If this is a 64-bit Windows system, we need to take different directory names into account
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
