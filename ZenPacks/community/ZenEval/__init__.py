
import Globals
import os.path
from os import system
import sys

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath

class ZenPack(ZenPackBase):
    def modifyLoginForm(self, text):
        login_form = zenPath('Products', 'ZenModel', 'skins', 'zenmodel', 'login_form.pt')
        login_form_f = open(login_form)
        login_form_lines = login_form_f.readlines()
        login_form_f.close()
        login_form_f = open(login_form, 'w')
        for line in login_form_lines:
            if "<body " in line:
                login_form_f.write(line[:line.find('<body ')+6] + text + line[line.find('document'):])
            else:
                login_form_f.write(line)
        login_form_f.close()

    def install(self, app):
        ZenPackBase.install(self, app)
        configFileName = zenPath('etc', 'zeneval.conf')
        if not os.path.exists(configFileName):
            configFile = open(configFileName, 'w')
            configFile.write('')
            configFile.close()
        self.dmd.zport.__setattr__('eval_expired', 'false')
        self.modifyLoginForm("tal:attributes=\"onload string:if (${here/eval_expired}) alert('Evaluation period is expired. Please, contact your distributor.');;")

    def remove(self, app, leaveObjects=False):
        self.dmd.zport.__delattr__('eval_expired')
        self.modifyLoginForm('onload="') 
        ZenPackBase.remove(self, app, leaveObjects)
