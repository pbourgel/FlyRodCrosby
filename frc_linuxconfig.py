#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc_linuxconfig.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the tools links and pgp keys information.
#####################################################################################

import os

home=os.path.expanduser("~")
gpg_file_name='gpg_to_install.tar.bz2'

hkps_cert_link=u'https://sks-keyservers.net/sks-keyservers.netCA.pem'
GPGurl=u'http://www.gnupg.org/download/'
tor_url = u'https://www.torproject.org/projects/torbrowser.html.en#Download-torbrowserbundle'
jitsi_url = u'https://download.jitsi.org/jitsi/debian/'
cryptocat_url = u'https://addons.mozilla.org/en-US/firefox/addon/cryptocat/'
enigmail_url = u'https://www.enigmail.net/download/download-static.php'
thunderbird_url = u'https://www.mozilla.org/en-US/thunderbird/all.html'
tails_url = u'https://tails.boum.org/download/'
torbirdy_xpi_url = u'https://www.torproject.org/dist/torbirdy/torbirdy-current.xpi'
torbirdy_xpi_sig_url = u'https://www.torproject.org/dist/torbirdy/torbirdy-current.xpi.asc'
url_trueCrypt=u'http://www.truecrypt.org/dl'
jitsi_url = u'https://jitsi.org/Main/Download'
jitsi_id = '0xC697D823EB0AB654'
FakeDomain_url=u'https://addons.mozilla.org/ro/firefox/addon/fake-domain/'

torbirdy_dev_gpg_fingerprint = u'228FAD203DE9AE7D84E25265CF9A6F914193A197'
tails_finger_print='0D24B36AA9A2A651787876451202821CBE2CD9C1'
tor_dev_gpg_fingerprint = '8738A680B84B3031A630F2DB416F061063FEE659'
enigmail_dev_gpg_fingerprint = u'10B2E4A0E718BB1B2791DAC4F040E41B9369CDF3'
tor_dev_gpg_name = u'Erinn Clark (erinn@torproject.org)'
gpg_servers = ['pool.sks-keyservers.net','subkeys.pgp.net','sks.mit.edu','pgp.mit.edu']

