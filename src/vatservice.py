# importing wx files
import wx
# import the newly created GUI file
import gui
# Import the vatservice library
import single
import batch
import helper

# import common libraries
import webbrowser
import json


# inherit from the MainFrame created in wxFowmBuilder and create CalcFrame
class CalcFrame(gui.MainFrame):
    # constructor
    def __init__(self, parent):
        # initialize parent class
        gui.MainFrame.__init__(self, parent)

    # load the config file
    def loadConfig(self, event):
        self.textUrl.SetValue(helper.load_value_from_json_file('url'))
        self.comboBoxInterface.SetValue(helper.load_value_from_json_file('interface'))
        self.comboBoxLanguage.SetValue(helper.load_value_from_json_file('language'))
        self.textCSVdelimiter.SetValue(helper.load_value_from_json_file('delimiter'))

        # load image from file
        image = wx.Image("../images/favicon.png", wx.BITMAP_TYPE_ANY)
        image = image.Scale(32, 32, wx.IMAGE_QUALITY_HIGH)
        bitmap = image.ConvertToBitmap()
        icon = wx.Icon()
        # set the image as icon for the frame
        icon.CopyFromBitmap(bitmap)
        self.SetIcon(icon)

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

    def vatserviceAbout(self, event):
        wx.MessageBox('vatservice-gui\n\nA simple GUI for the vatservice library.',
                      'About vatservice-gui',
                      wx.OK | wx.ICON_INFORMATION)

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
        wx.MessageBox('Start the batch validation.', 'Batch Validation', wx.OK | wx.ICON_INFORMATION)
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


# mandatory in wx, create an app, False stands for not deteriction stdin/stdout
# refer manual for details
app = wx.App(False)

# create an object of CalcFrame
frame = CalcFrame(None)

# show the frame
frame.Show(True)

# start the applications
app.MainLoop()
