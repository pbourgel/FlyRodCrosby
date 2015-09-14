#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc_winconfig.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains tools details: download links and pgp
#                   signatures.
##################################################################################


import os

macGPGurl= u'https://gpgtools.org/'
tor_url = u'https://www.torproject.org/projects/torbrowser.html.en#Download-torbrowserbundle'
jitsi_url = u'https://jitsi.org/Main/Download'

#SOMEONE PLEASE CHECK THAT I GOT ERINN CLARK'S GPG INFO RIGHT
tor_dev_gpg_fingerprint = '8738A680B84B3031A630F2DB416F061063FEE659'
tor_dev_gpg_name = u'Erinn Clark (erinn@torproject.org)'
enigmail_dev_gpg_fingerprint = u'10B2E4A0E718BB1B2791DAC4F040E41B9369CDF3'
gpg_servers = ['pool.sks-keyservers.net','subkeys.pgp.net','sks.mit.edu','pgp.mit.edu']

#TO-DO: We need to substitute whatever the language variable needs to be in here
cryptocat_url = u'https://addons.mozilla.org/en-US/firefox/addon/cryptocat/'
enigmail_url = u'https://www.enigmail.net/download/download-static.php'
thunderbird_url = u'https://www.mozilla.org/en-US/thunderbird/all.html'
bleachbit_url = u'http://bleachbit.sourceforge.net/download/windows'
bleachbit_base_url = u'http://bleachbit.sourceforge.net/download/'
tails_url = u'https://tails.boum.org/download/'
torbirdy_xpi_url = u'https://www.torproject.org/dist/torbirdy/torbirdy-current.xpi'
torbirdy_xpi_sig_url = u'https://www.torproject.org/dist/torbirdy/torbirdy-current.xpi.asc'
torbirdy_dev_gpg_fingerprint = u'228FAD203DE9AE7D84E25265CF9A6F914193A197'
url_trueCrypt=u'http://www.truecrypt.org/dl'
jitsi_url = u'https://jitsi.org/Main/Download'
tails_finger_print='0D24B36AA9A2A651787876451202821CBE2CD9C1'
FakeDomain_url=u'https://addons.mozilla.org/ro/firefox/addon/fake-domain/'
