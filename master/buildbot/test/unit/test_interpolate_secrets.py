from __future__ import absolute_import
from __future__ import print_function

from twisted.trial import unittest

from buildbot.process.properties import Interpolate
from buildbot.secrets.provider.base import SecretProviderBase
from buildbot.test.fake import fakemaster


class FakeSecretStorage(SecretProviderBase):

    def __init__(self, allsecretsInADict):
        self.allsecrets = allsecretsInADict

    def get(self, key):
        if key in self.allsecrets:
            return self.allsecrets[key], None
        else:
            return None, None


class TestInterpolateSecrets(unittest.TestCase):

    def setUp(self):
        self.master = fakemaster.make_master()
        self.master.config.secretsManagers = [FakeSecretStorage({"foo": "bar",
                                                                 "other": "value"})]

    def testInterpolate(self):
        secrets = Interpolate('echo %(secrets:foo)s')
        print("secrets:", secrets)
