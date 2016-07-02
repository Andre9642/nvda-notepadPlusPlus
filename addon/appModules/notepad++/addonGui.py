#addonGui.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx

import addonHandler
import config
import gui

addonHandler.initTranslation()

"""File for managing GUI for the appModule for notepad++"""

class GuiManager(object):

	def __init__(self):
		def _popupMenu(evt):
			gui.mainFrame._popupSettingsDialog(SettingsDialog)
		self.prefsMenuItem  = item = gui.mainFrame.sysTrayIcon.preferencesMenu.Append(wx.ID_ANY, _("Notepad++..."))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, _popupMenu, item)

	def enableItem(self):
		self.prefsMenuItem.Enable(True)

	def disableItem(self):
		self.prefsMenuItem.Enable(False)

	def __del__(self):
		try:
			gui.mainFrame.sysTrayIcon.preferencesMenu.RemoveItem(self.prefsMenuItem)
		except wx.PyDeadObjectError:
			pass

class SettingsDialog(gui.SettingsDialog):
	# Translators: Title for the settings dialog
	title = _("Notepad++ settings")

	def __init__(self, *args, **kwargs):
		super(SettingsDialog, self).__init__(*args, **kwargs)

	def makeSettings(self, settingsSizer):
		# Translators: A setting for enabling/disabling line length indicator.
		self.lineLengthIndicatorCheckBox = wx.CheckBox(self, wx.NewId(), label=_("Enable &line length indicator"))
		self.lineLengthIndicatorCheckBox.SetValue(config.conf["notepadPp"]["lineLengthIndicator"])
		settingsSizer.Add(self.lineLengthIndicatorCheckBox, border=10, flag=wx.BOTTOM)
		maxLineLengthSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Setting for maximum line length used by line length indicator
		maxLineLengthLabel = wx.StaticText(self, -1, label=_("&Maximum line length:"))
		self.maxLineLengthEdit = wx.TextCtrl(self, wx.NewId())
		self.maxLineLengthEdit.SetValue(str(config.conf["notepadPp"]["maxLineLength"]))
		maxLineLengthSizer.AddMany([maxLineLengthLabel, self.maxLineLengthEdit])
		settingsSizer.Add(maxLineLengthSizer, border=10, flag=wx.BOTTOM)

	def postInit(self):
		self.lineLengthIndicatorCheckBox.SetFocus()

	def onOk(self, evt):
		config.conf["notepadPp"]["lineLengthIndicator"] = self.lineLengthIndicatorCheckBox.IsChecked()
		config.conf["notepadPp"]["maxLineLength"] = int(self.maxLineLengthEdit.GetValue())
		super(SettingsDialog, self).onOk(evt)
