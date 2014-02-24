FlyRodCrosby
============

Making Cryptoparties easier since 1897!

FlyRodCrosby[1] is an automated installer for Windows (stay tuned for an OSX port) for all of the standard Cryptoparty tools.  It currently handles:

GPG4Win

Tor Browser Bundle [3]

Thunderbird with Enigmail [2]

Jitsi [4]

TorBirdy [5]

We plan to support:

Bleachbit [6]

TrueCrypt [7]

Functionality to automatically download Tails [8] and burn it to a DVD

The Fake Domain Detective plugin from Access[9]

To build FlyRodCrosby from source, install PyInstaller and type

~~~
pyinstaller frc_gui.py --onefile
~~~

The EXE will be stored in the dist subfolder.  When running the EXE, run as Administrator and include the certificate file associated with the requests library.  On Python 2.7.x this is usually found in C:\Python27\Lib\site-packages\requests\cacert.pem

Note to potential developers
============================

When making an application available for download/install that has a detached GPG signature, remember to add the full fingerprint rather than the 8 character ID due to the security issue described in [10].


[1] https://en.wikipedia.org/wiki/Cornilia_Thurza_Crosby

[2] https://www.enigmail.net/home/index.php

[3] https://www.torproject.org/

[4] https://jitsi.org/

[5] https://trac.torproject.org/projects/tor/wiki/torbirdy

[6] http://bleachbit.sourceforge.net/

[7] http://www.truecrypt.org/

[8] https://tails.boum.org/

[9] https://addons.mozilla.org/en-US/firefox/addon/fake-domain/

[10] http://www.asheesh.org/note/debian/short-key-ids-are-bad-news.html
