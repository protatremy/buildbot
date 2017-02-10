# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from __future__ import absolute_import
from __future__ import print_function

import os

import mock

from twisted.internet import defer
from twisted.trial import unittest

from buildbot.secrets.provider.file import SecretInAFile
from buildbot.test.util.config import ConfigErrorsMixin


class TestSecretInFile(ConfigErrorsMixin, unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        self.srvfile = SecretInAFile("name", "/path/todirname", ext=None)
        yield self.srvfile.startService()

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.srvfile.stopService()

    def testCheckConfigSecretInAFileService(self):
        self.assertEqual(self.srvfile.name, "SecretInAFile")
        self.assertEqual(self.srvfile._dirname, "/path/todirname")

    def testCheckConfigErrorSecretInAFileService(self):
        self.assertRaisesConfigError("directory name could not be empty",
         lambda: self.srvfile.checkConfig("name2", None, ext=None))

    @defer.inlineCallbacks
    def testReconfigSecretInAFileService(self):
        yield self.srvfile.reconfigService("name2", "/path/todirname2", ext=None)
        self.assertEqual(self.srvfile.name, "SecretInAFile")
        self.assertEqual(self.srvfile._dirname, "/path/todirname2")

    def testGetFile(self):
        self.mktemp -->> a voir pour eviter le mock
        os.path.isfile = mock.Mock(True)
        open = mock.Mock("something")
        value = self.srvfile.get("kiki")
