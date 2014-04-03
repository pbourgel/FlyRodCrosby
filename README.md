FlyRodCrosby
============

Making Cryptoparties easier since 1897!

FlyRodCrosby[1] is an automated installer for Windows (stay tuned for an OSX port) for all of the standard Cryptoparty tools.  It currently handles:

macGPG[2]

Tor Browser Bundle [3]

Thunderbird with Enigmail [2]

Jitsi [5]

TorBirdy [6]

Cryptocat [4]

Bleachbit [7]

TrueCrypt [8]

Functionality to automatically download Tails [9] and burn it to a DVD

[1] https://en.wikipedia.org/wiki/Cornilia_Thurza_Crosby

[2] https://www.enigmail.net/home/index.php

[3] https://www.torproject.org/

[4] https://crypto.cat/

[5] https://jitsi.org/

[6] https://trac.torproject.org/projects/tor/wiki/torbirdy

[7] http://bleachbit.sourceforge.net/

[8] http://www.truecrypt.org/

[9] https://tails.boum.org/


making the .app file
====================
We use py2app:<br>
  in your terminal :<br>
    1-pip install py2app<br>
    2-py2applet --make-setup path/to/the/FlyRodCrosby/frc-gui.py #this will make the setup.py file on your home directory<br>
    3-python setup.py py2app --arch=universal #this willl generate two directory build/ and dist/ you can check the applcation on buil/<br>
					      #arch can be more spcified '--arch=VALUE' where VALUE is the architecture type:<br>
					      #fat: i386, ppc<br>
					      #fat3: i386, x86_64, ppc<br>
					      #univeral: i386, x86_64, ppc, ppc64<br>
					      #intel: i386, x86_64<br>

