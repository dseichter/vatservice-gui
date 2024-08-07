# Copyright (c) 2024 Daniel Seichter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# importing wx files
import wx
# import the newly created GUI file
import gui
# Import the vatservice library
import single
import batch
import helper
import about_ui
import icons

# import common libraries
import webbrowser
import json


# inherit from the MainFrame created in wxFowmBuilder and create CalcFrame
class CalcFrame(gui.MainFrame):
    # constructor
    def __init__(self, parent):
        # initialize parent class
        gui.MainFrame.__init__(self, parent)

        # add the version to the label
        self.SetTitle(helper.NAME + ' ' + helper.VERSION)

        # specify all the icons
        gui.MainFrame.SetIcon(self, icons.tick_box.GetIcon())
        self.menuitemFileClose.SetBitmap(icons.cancel.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        self.menuitemHelpSupport.SetBitmap(icons.get_help.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        self.menuitemHelpUpdate.SetBitmap(icons.restart.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        self.menuitemHelpAbout.SetBitmap(icons.info.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        self.m_notebook3.SetSelection(0)
        # create image list
        self.imageList = wx.ImageList(16, 16)
        # add the icons
        self.imageList.Add(icons.document.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        self.imageList.Add(icons.microsoft_excel.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        self.imageList.Add(icons.settings.GetBitmap().ConvertToImage().Rescale(16, 16).ConvertToBitmap())
        # set the image list
        self.m_notebook3.AssignImageList(self.imageList)
        # set the icons
        self.m_notebook3.SetPageImage(0, 0)
        self.m_notebook3.SetPageImage(1, 1)
        self.m_notebook3.SetPageImage(2, 2)

    # load the config file
    def loadConfig(self, event):
        self.textUrl.SetValue(helper.load_value_from_json_file('url'))
        self.comboBoxInterface.SetValue(helper.load_value_from_json_file('interface'))
        self.comboBoxLanguage.SetValue(helper.load_value_from_json_file('language'))
        self.textCSVdelimiter.SetValue(helper.load_value_from_json_file('delimiter'))

    # save the config file
    def saveConfig(self, event):
        # open the file
        with open('config.json', 'w') as f:
            # write the data
            f.write(json.dumps({
                'url': self.textUrl.GetValue(),
                'interface': self.comboBoxInterface.GetValue(),
                'language': self.comboBoxLanguage.GetValue(),
                'delimiter': self.textCSVdelimiter.GetValue()
            }, indent=2))

    # put a blank string in text when 'Clear' is clicked
    def clearFunc(self, event):
        self.textOwnvat.SetValue(str(''))
        self.textForeignvat.SetValue(str(''))
        self.textCompany.SetValue(str(''))
        self.textStreet.SetValue(str(''))
        self.textZip.SetValue(str(''))
        self.textTown.SetValue(str(''))
        self.textResultIsValid.SetValue(str(''))
        self.textResultCode.SetValue(str(''))
        self.textResultDetails.SetValue(str(''))

    def vatserviceClose(self, event):
        self.Close()

    def vatserviceGitHub(self, event):
        webbrowser.open_new_tab('https://github.com/dseichter/vatservice-gui')  # Add the URL of the GitHub repository

    def validateSingle(self, event):
        wx.MessageBox('Start the single validation.', 'Single Validation', wx.OK | wx.ICON_INFORMATION)
        returncode, message = single.validatesingle(ownvat=self.textOwnvat.GetValue(),
                                                    foreignvat=self.textForeignvat.GetValue(),
                                                    company=self.textCompany.GetValue(),
                                                    street=self.textStreet.GetValue(),
                                                    zip=self.textZip.GetValue(),
                                                    town=self.textTown.GetValue(),
                                                    type=helper.load_value_from_json_file('interface'),
                                                    lang=helper.load_value_from_json_file('language'))
        message = json.loads(message)
        self.textResultIsValid.SetValue(str(message['valid']))
        self.textResultCode.SetValue(str(returncode))
        self.textResultDetails.SetValue(json.dumps(message, indent=2))

    def validateBatch(self, event):
        if wx.MessageBox('Are you sure you want to start the batch validation?', 'Batch Validation', wx.YES_NO | wx.ICON_HAND) == wx.NO:
            return

        if self.m_filePickerOutput.GetPath() == '':
            wx.MessageBox('Please select an output file.', 'No output file', wx.OK | wx.ICON_ERROR)
            return

        batch.validatebatch(inputfile=self.filePickerInput.GetPath(),
                            outputfile=self.m_filePickerOutput.GetPath(),
                            type=helper.load_value_from_json_file('interface'),
                            lang=helper.load_value_from_json_file('language'))

    def checkForUpdates(self, event):
        if helper.check_for_new_release():
            result = wx.MessageBox('A new release is available.\nWould you like to open the download page?', 'Update available', wx.YES_NO | wx.ICON_INFORMATION)
            if result == wx.YES:
                webbrowser.open_new_tab(helper.RELEASES)
        else:
            wx.MessageBox('No new release available.', 'No update', wx.OK | wx.ICON_INFORMATION)

    def vatserviceAbout(self, event):
        # open the about dialog
        dlg = about_ui.DialogAbout(self)
        dlg.ShowModal()
        dlg.Destroy()


# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
app = wx.App(False)

# create an object of CalcFrame
frame = CalcFrame(None)

# show the frame
frame.Show(True)

# start the applications
app.MainLoop()
