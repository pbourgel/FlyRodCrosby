#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name            : frc-gui.py
# Version         : 0.2
# Author          : Peter Bourgelais
# Date            : 20131016
# Owner           : Peter Bourgelais
# License         : GPLv2
# Description     : This component contains the graphical user interface classes.
#################################################################################

import os
import wx

from frc_windows import *
from langauges import *


l = ["en-US",'fr', 'ar', 'es', "it", 'ru']

class LangPanel(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.ok = wx.Button(self, -1, label = "OK",
                            pos=wx.Point(210,50))
        self.exit = wx.Button(self, -1, label = "EXIT",
                              pos=wx.Point(300,50))
        self.ok.Bind(wx.EVT_BUTTON, self.okClick, self.ok)
        self.exit.Bind(wx.EVT_BUTTON, self.exitClick, self.exit)
        wx.StaticText(self, -1, "Choose language:", (10,30))
        self.combo=wx.ComboBox(self,-1,
                               value=l[0],
                               pos=wx.Point(10,50),
                               choices=l,
                               style=wx.CB_READONLY)

    # This method is called when OK button is clicked
    def okClick(self, e):
	global lang
        lang = self.combo.GetValue()
        lang_frame.Destroy()
                
    # This method is called when EXIT button is clicked
    def exitClick(self, e):
	exit()


class FRCMainFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.desc = wx.StaticText(self, -1, First_msg(lang).getFirstMsg())
	self.desc.Wrap(400)
        self.tbird_checkbox = wx.CheckBox(self, -1, tbird_checkbox_msg(lang).getCheckBoxLabel())
        self.tbb_checkbox = wx.CheckBox(self, -1, tbb_checkbox_msg(lang).getCheckBoxLabel())
        self.torbirdy_checkbox = wx.CheckBox(self, -1,torbirdy_checkbox_msg(lang).getCheckBoxLabel())
        self.jitsi_checkbox = wx.CheckBox(self, -1, jitsi_checkbox_msg(lang).getCheckBoxLabel())
	self.CryptoCat_checkbox = wx.CheckBox(self, -1,CryptoCat_checkbox_msg(lang).getCheckBoxLabel())	
        self.ok_button = wx.Button(self, wx.ID_OK, "OK")
        self.cancel_button = wx.Button(self, wx.ID_CLOSE, "Quit")
        self.SetBackgroundColour(wx.WHITE)
        self.__set_properties()
        self.__do_layout()
   
    
    def __set_properties(self):
        self.SetTitle("FlyRodCrosby - Making Cryptoparties easier since 1897!")
        self.SetSize((1000,500))
        self.SetBackgroundColour('#ededed')
        

    def __do_layout(self):
        item_border = 5
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(1, 2, 0, 0)
        sizer_1.Add(self.desc, 1, wx.ALL, item_border)
        sizer_1.Add(self.tbird_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.tbb_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.torbirdy_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.jitsi_checkbox, 0, wx.ALL, item_border)
        sizer_1.Add(self.CryptoCat_checkbox, 0, wx.ALL, item_border)
        grid_sizer_1.Add(self.ok_button, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 0)
        grid_sizer_1.Add(self.cancel_button, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.ALIGN_RIGHT, 5)
        self.SetSizer(sizer_1)
        self.Bind(wx.EVT_BUTTON, self.onClose, self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.installationController, self.ok_button)
        self.Layout()
        self.Show(True)

    # This method is called when CLOSE button is clicked
    def onClose(self, evt):
        self.Close(True)

    # This method is called when INSTALL button is clicked. It will install
    # the checked tools. 
    def installationController(self, evt):
      
        if self.tbird_checkbox.IsChecked():
            getThunderbirdWithEnigmail()

        if self.CryptoCat_checkbox.IsChecked():
	    downloadCryptoCat()
            installCryptoCat()

        if self.tbb_checkbox.IsChecked():
            getTOR(tor_url,'en-US')

        if self.jitsi_checkbox.IsChecked():
            getJitsi()

        if self.torbirdy_checkbox.IsChecked():
            getTorBirdy()
            installTorBirdy()


# Main routine
lang_app = wx.PySimpleApp()
lang_frame = wx.Frame(None, -1, "FlyRodCrosby", pos=wx.Point(500,200),
                      size=(400,150), style= wx.MINIMIZE)
LangPanel(lang_frame, -1)
lang_frame.Show(True)
lang_app.MainLoop()

main_app = wx.App()
main_frame = FRCMainFrame(None, -1, 'FlyRodCrosby-Making Cryptoparties easier since 1897!',
                          style= wx.MINIMIZE,pos=(150,150))
main_app.SetTopWindow(main_frame)
main_frame.Show()
main_app.MainLoop()

