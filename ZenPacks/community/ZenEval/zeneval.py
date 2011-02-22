#!/usr/bin/env python

import Globals
import transaction
import os
from time import time, mktime, strptime

from Products.ZenUtils.CyclingDaemon import CyclingDaemon
from Products.ZenUtils.Utils import zenPath
from twisted.internet import reactor

class ZenEval(CyclingDaemon):
    name = 'ZenEval'
    def buildOptions(self):
        CyclingDaemon.buildOptions(self)
        self.parser.add_option('--duration', dest='duration', type='int', default=60, help='Duration of evaluation period')

    def __init__(self):
        CyclingDaemon.__init__(self)
        self.options.cycletime *= 2
        log = open(os.path.join(zenPath('log'),'install.log'))
        for line in log:
            if 'Fresh install pre steps' in line:
                self.installDate = mktime(strptime(log.next(),'%a %b %d %H:%M:%S %Z %Y\n'))
                break
        self.log.info('Started')

    def main_loop(self):
        self.log.info('Checking evaluation period...')
        if self.installDate + self.options.duration * 3600 * 24 < time() and self.dmd.zport.eval_expired=='false':
            self.endEval()

    def endEval(self):
        self.log.info('Evaluation period is expired. Blocking all users...')
        from string import letters, digits
        from random import choice
        size=8
        for user in [user.viewName() for user in self.dmd.ZenUsers.getAllUserSettings()]:
            try:
                self.dmd.zport.acl_users.userManager.updateUserPassword(user, ''.join([choice(letters + digits) for i in range(size)]))
            except KeyError:
                self.app.acl_users.userManager.updateUserPassword(user, ''.join([choice(letters + digits) for i in range(size)]))
        self.dmd.zport.eval_expired='true'
        transaction.commit()

if __name__ == "__main__":
    ze = ZenEval()
    ze.run()
