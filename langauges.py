# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : languages.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the text messages with different languages.
#######################################################################################

class fct():
	def __init__(self,lg):
		self.lang=lg

	msgEN=''
	msgFR=''
	msgES=''
	msgIT=''
	msgAR=''
	msgRU=''

      	First_msgEN=''
        First_msgFR=''
        First_msgES=''
        First_msgIT=''
        First_msgAR=''
        First_msgRU=''

	def getFirstMsg(self):
		if (self.lang=='en-US'):
			return self.First_msgEN
		if(self.lang=='fr'):
			return self.First_msgFR
		if (self.lang=='es'):
                        return self.First_msgES
		if (self.lang=='it'):
                        return self.First_msgIT
		if (self.lang=='ar'):
                        return self.First_msgAR
		if (self.lang=='ru'):
                        return self.First_msgRU
	
	def getCheckBoxLabel(self):
                if (self.lang=='en-US'):
                        return self.msgEN
                if(self.lang=='fr'):
                        return self.msgFR
                if (self.lang=='es'):
                        return self.msgES
                if (self.lang=='it'):
                        return self.msgIT
                if (self.lang=='ar'):
                        return self.msgAR
                if (self.lang=='ru'):
                        return self.msgRU



class First_msg(fct):
	First_msgEN="Welcome to FlyRodCrosby, an auto-installer for standard secure communications tools.\nSelect the apps you want to install below and click OK to begin the installation process."
	First_msgFR="Bienvenue à FlyRodCrosby, un auto-installeur pour des outils standard de communications sécurisées.\nSelectionnez les applications que vous souhaitez installer ci-dessous et cliquez sur OK pour commencer le processus d'installation."
	First_msgES="Bienvenido a FlyRodCrosby, un instalador automático de herramientas de comunicación seguras estándar.\nSeleccione las aplicaciones que desea instalar a continuación y haga clic en Aceptar para comenzar el proceso de instalación."
	First_msgIT="Benvenuti a FlyRodCrosby, un auto-installer per gli strumenti di comunicazione sicuri standard.\nSelezionare le applicazioni che si desidera installare sotto e fare clic su OK per avviare il processo di installazione."
	First_msgAR="مرحبا بكم في FlyRodCrosby، وهو المثبت السيارات لأدوات الاتصالات المؤمنة القياسية. حدد التطبيقات التي ترغب في تثبيت أدناه وانقر فوق موافق لبدء عملية التثبيت."
	First_msgRU="Добро пожаловать в FlyRodCrosby, авто-установки для стандартных инструментов безопасных коммуникаций.\nВыберите приложения, которые требуется установить ниже и нажмите кнопку ОК, чтобы начать процесс установки."
	

class tbird_checkbox_msg(fct):
	msgEN="Thunderbird with Enigmail lets you send and receive encrypted emails."
	msgFR="Thunderbird avec Enigmail vous permet d'envoyer et de recevoir des e-mails cryptés."
	msgES="Thunderbird con Enigmail te permite enviar y recibir mensajes de correo electrónico cifrados."
	msgIT="Thunderbird con Enigmail consente di inviare e ricevere messaggi di posta elettronica crittografati."
	msgAR="Thunderbird مع Enigmail يتيح لك إرسال واستقبال رسائل البريد الإلكتروني مشفرة."
	msgRU="Thunderbird с Enigmail позволяет отправлять и получать зашифрованные сообщения электронной почты."

class tbb_checkbox_msg(fct):
        msgEN="The Tor Browser Bundle lets you browse the web anonymously."
        msgFR="Le navigateur Tor Bundle vous permet de naviguer sur le Web de façon anonyme."
        msgES="El Tor Browser Bundle le permite navegar por la web de forma anónima."
        msgIT="Il Browser Bundle Tor permette di navigare il web in forma anonima."
        msgAR="إن حزمة متصفح تور يتيح لك تصفح الانترنت مجهول الهوية"
        msgRU="Browser Bundle Тор позволяет просматривать веб-страницы анонимно."

class torbirdy_checkbox_msg(fct):
        msgEN="TorBirdy lets you send and receive email over the Tor network (requires Tor and Thunderbird)."
        msgFR="TorBirdy vous permet d'envoyer et de recevoir des e-mails sur le réseau Tor (nécessite Tor et Thunderbird)."
        msgES="TorBirdy le permite enviar y recibir correo electrónico a través de la red Tor (requiere Tor y Thunderbird)."
        msgIT="TorBirdy consente di inviare e ricevere mail tramite la rete Tor (richiede Tor e Thunderbird)."        
        msgAR="TorBirdy يتيح لك إرسال واستقبال البريد الإلكتروني عبر شبكة تور (tor يتطلب و thunderbird)."
        msgRU="TorBirdy позволяет отправлять и получать электронную почту по сети Tor (требуется Tor и Thunderbird)."

class jitsi_checkbox_msg(fct):
        msgEN="Jitsi is a secure Skype alternative with support for encrypted chat."
        msgFR="Jitsi est une alternative Skype sécurisé avec un support pour le chat crypté."
        msgES="Jitsi es una alternativa segura Skype con soporte para el chat encriptado."
        msgIT="Jitsi è un'alternativa sicura Skype con il supporto per la chat criptata."
        msgAR="Jitsi هو بديل آمن سكايب مع دعم لدردشة مشفرة."
        msgRU="Jitsi является безопасной альтернативой Skype с поддержкой зашифрованный чат."

class truecrypt_checkbox_msg(fct):
        msgEN="Use Truecrypt to encrypt files on your computer."
        msgFR="Utiliser TrueCrypt pour crypter les fichiers sur votre ordinateur."
        msgES="Usar TrueCrypt para cifrar archivos en su ordenador."
        msgIT="Usa Truecrypt per crittografare i file sul vostro computer."        
        msgAR="استخدام تروكربت لتشفير الملفات الموجودة على جهاز الكمبيوتر الخاص بك."
        msgRU="Использовать TrueCrypt для шифрования файлов на вашем компьютере."

class tailsISO_checkbox_msg(fct):
        msgEN="Download Tails and burn it to a DVD for a temporary Windows alternative in highly insecure environments."
        msgFR="Télécharger Tails et le graver sur un DVD pour une alternative temporaire de Windows dans des environnements hautement sécurisés."
        msgES="Descarga colas y grabarlo en un DVD de una alternativa temporal de Windows en entornos altamente inseguros."
        msgIT="Scarica Tails e masterizzarlo su un DVD per una temporanea di Windows un'alternativa in ambienti altamente insicuri."        
        msgAR="تحميل Tails ونسخ إلى قرص DVD بديل   عن ويندوز مؤقتة في بيئات غير آمنة للغاية."
        msgRU="Скачать хвосты и записать его на DVD для временного альтернативы Windows, в высоко опасных условиях."

class bleachbit_checkbox_msg(fct):
        msgEN="Bleachbit securely deletes sensitive files to prevent recovery."
        msgFR="Bleachbit supprime solidement les dossiers sensibles pour éviter la reprise."
        msgES="Bleachbit suprime con seguridad archivos sensibles para impedir la recuperación."
        msgIT="BleachBit cancella in modo sicuro i file sensibili per prevenire il recupero."        
        msgAR="Bleachbit بشكل آمن يحذف الملفات الحساسة لمنع الانتعاش."
        msgRU="Bleachbit надежно удаляет важные файлы, что препятствует восстановлению."

class truecrypt_checkbox_msg(fct):
        msgEN="Use Truecrypt to encrypt files on your computer."
        msgFR="Utiliser TrueCrypt pour crypter les fichiers sur votre ordinateur."
        msgES="Usar TrueCrypt para cifrar archivos en su ordenador."
        msgIT="Usa Truecrypt per crittografare i file sul vostro computer."        
        msgAR="استخدام تروكربت لتشفير الملفات الموجودة على جهاز الكمبيوتر الخاص بك."
        msgRU="Использовать TrueCrypt для шифрования файлов на вашем компьютере."
	
class fakeOut_checkbox_msg(fct):
        msgEN="The FakeOut plugin from Access prevents Fake Domain attacks caused by misspelled domain names and other network shenanigans."
        msgFR="Le plugin fakeout de Access Now empêche les attaques de domaine faux causés par les noms de domaine mal orthographiés et autres manigances du réseau."
        msgES="El plugin Fakeout de AccessNow previene los ataques de dominio falsos causados por los nombres de dominio con errores ortográficos y otros chanchullos de la red."
        msgIT="Il plugin Fakeout da AccessNow previene gli attacchi di dominio falsi causati da errate nomi di dominio e altri imbrogli di rete."        
        msgAR="البرنامج المساعد FakeOut من AccessNow يمنع هجمات وهمية المجال الناجمة عن أسماء النطاقات التي بها أخطاء إملائية والاشكالات شبكة أخرى."
        msgRU="FakeOut плагин от AccessNow предотвращает Поддельные атаки домена, вызванных ошибками доменных имен и других сетевых махинаций."

class CryptoCat_checkbox_msg(fct):
        msgEN="Cryptocat uses modern web technologies to provide easy to use, accessible encrypted chat with your friends, right in your browser. "
        msgFR="Cryptocat utilise des technologies Web modernes pour fournir facile à utiliser, le chat cryptée accessible avec vos amis, directement dans votre navigateur."
        msgES="Cryptocat utiliza tecnologías web modernas para proporcionar un fácil de usar, el chat encriptado accesible con tus amigos, en tu navegador."
        msgIT="Cryptocat utilizza tecnologie web moderne per fornire un facile da usare, accessibili chat crittata con i tuoi amici, direttamente dal tuo browser."        
        msgAR='cryptocat تقنيات الويب الحديثة لتوفير سهلة الاستخدام، ويمكن الوصول إليها مشفرة دردشة مع أصدقائك، والحق في المتصفح الخاص بك.'
	msgRU='Cryptocat использует современные веб-технологии, чтобы обеспечить легкий в использовании, доступную зашифрованный чат с друзьями, прямо в браузере.'
