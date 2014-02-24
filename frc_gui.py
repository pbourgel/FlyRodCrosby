#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Tue Nov 26 15:06:57 2013
#Fly Rod Crosby: Making Cryptoparties Easier since 1897!
import wx
import os
import sys
import subprocess
import ctypes

from frc_windows import *

# begin wxGlade: extracode
# end wxGlade

item_border=5
tab_offset=10

# A note on dependencies:
# Thunderbird, Enigmail, and GPG4Win / MacGPG all need to be installed together
# x --> y means x depends on y
# TorBirdy --> Thunderbird and Tor
# Everything with a GPG signature --> GPG4Win/MacGPG

class FRCMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: FRCMainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.combo_box_1 = wx.ComboBox(self, -1, choices=["English", u"العربية", u"Français", u"Español", u"Português"], style=wx.CB_READONLY)
        self.label_1 = wx.StaticText(self, -1, "Welcome to FlyRodCrosby, an auto-installer for standard secure communications tools.  Select the apps you want to install below and click OK to begin the installation process.")
        self.label_1.Wrap(400)
        self.tbird_checkbox = wx.CheckBox(self, -1, "Thunderbird with Enigmail lets you send and receive encrypted emails.")
        self.tbb_checkbox = wx.CheckBox(self, -1, "The Tor Browser Bundle lets you browse the web anonymously.")
        self.torbirdy_checkbox = wx.CheckBox(self, -1, "TorBirdy lets you send and receive email over the Tor network (requires Tor and Thunderbird).")
        self.jitsi_checkbox = wx.CheckBox(self, -1, "Jitsi is a secure Skype alternative with support for encrypted chat.")
        self.bleachbit_checkbox = wx.CheckBox(self, -1, "Bleachbit securely deletes sensitive files to prevent recovery.")
        self.truecrypt_checkbox = wx.CheckBox(self, -1, "Use Truecrypt to encrypt files on your computer.")
        self.tailsISO_checkbox = wx.CheckBox(self, -1, "Download Tails and burn it to a DVD for a temporary Windows alternative in highly insecure environments.")
        self.fakeOut_checkbox = wx.CheckBox(self, -1, "The FakeOut plugin from Access prevents Fake Domain attacks caused by misspelled domain names and other network shenanigans.")
        self.ok_button = wx.Button(self, wx.ID_OK, "OK")
        self.cancel_button = wx.Button(self, wx.ID_CLOSE, "Quit")
        self.SetBackgroundColour(wx.WHITE)



        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FRCMainFrame.__set_properties
        self.SetTitle("FlyRodCrosby - Making Cryptoparties easier since 1897!")
        self.SetSize((640, 412))
        self.combo_box_1.SetSelection(-1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FRCMainFrame.__do_layout
        global item_border
        global tab_offset
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(1, 2, 0, 0)
        sizer_1.Add(self.combo_box_1, 0, wx.ALIGN_RIGHT, item_border)
        sizer_1.Add(self.label_1, 0, wx.ALL, item_border)
        sizer_1.Add(self.tbird_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.tbb_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.torbirdy_checkbox, 0, wx.ALL, item_border+tab_offset)
        sizer_1.Add(self.jitsi_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.bleachbit_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.truecrypt_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.tailsISO_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.fakeOut_checkbox, 0, wx.ALL, item_border)
        grid_sizer_1.Add(self.ok_button, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 0)
        grid_sizer_1.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.ALIGN_RIGHT, 5)
        self.SetSizer(sizer_1)

        self.Bind(wx.EVT_BUTTON, self.on_close, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.installation_controller, self.ok_button)
        
        # end wxGlade
        self.Layout()
        self.Show(True)


    def on_close(self, evt):
        self.Close(True)

    def installation_controller(self, evt):
      
        if self.tbird_checkbox.IsChecked():
            getThunderbirdWithEnigmail('en-US', self.torbirdy_checkbox.IsChecked())

        if self.tbb_checkbox.IsChecked():
            getTOR(tor_url,'en-US')

        if self.jitsi_checkbox.IsChecked():
            getJitsi(jitsi_url)

        if self.torbirdy_checkbox.IsChecked():
            getTorBirdy()
            installTorBirdy()

        if self.bleachbit_checkbox.IsChecked():
            getBleachBit()

        if self.tailsISO_checkbox.IsChecked():
            getTailsISO()

        if self.truecrypt_checkbox.IsChecked():
            getTrueCrypt()

        if self.fakeOut_checkbox.IsChecked():
            getFakeOut()


# end of class FRCMainFrame
FRCAlert('Running main loop\n')
app = wx.App()
frame_1 = FRCMainFrame(None, -1, "")
app.SetTopWindow(frame_1)
#frame_1.Show()
app.MainLoop()
#close_input = raw_input('Press Enter to quit')