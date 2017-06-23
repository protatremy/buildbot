from __future__ import absolute_import
from __future__ import print_function

from twisted.internet import defer
from twisted.trial import unittest

from buildbot.process.properties import Secret
from buildbot.secrets.manager import SecretManager
from buildbot.test.fake import fakemaster
from buildbot.test.fake.fakebuild import FakeBuild
from buildbot.test.fake.secrets import FakeSecretStorage
from buildbot.util.service import BuildbotService


class FakeBuildWithMaster(FakeBuild):

    def __init__(self, master):
        super(FakeBuildWithMaster, self).__init__()
        self.master = master


class FakeServiceUsingSecrets(BuildbotService):

    name = "FakeServiceUsingSecrets"

    def reconfigService(self, *args, **kwargs):
        self.kwargs = kwargs
        print("[DEBUG] kwargs in fake service", self.kwargs)

    def returnRenderedSecrets(self, secretKey):
        try:
            print("return")
            # return self.kwargs[secretKey]
        except Exception:
            raise Exception


class TestRenderSecrets(unittest.TestCase):

    def setUp(self):
        self.master = fakemaster.make_master()
        fakeStorageService = FakeSecretStorage()
        fakeStorageService.reconfigService(secretdict={"foo": "bar",
                                                       "other": "value"})
        self.secretsrv = SecretManager()
        self.buildbotservice_m = SecretManager()
        self.secretsrv.services = [fakeStorageService]
        self.secretsrv.setServiceParent(self.master)
        self.srvtest = FakeServiceUsingSecrets()
        self.srvtest.setServiceParent(self.master)
        self.successResultOf(self.master.startService())

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.srvtest.stopService()
        yield self.secretsrv.stopService()

    @defer.inlineCallbacks
    def test_secret_rendered(self):
        print("[DEBUG] beuytuyt")

        yield self.srvtest.reconfigService(secret=Secret("foo"))
        self.master.reconfigServiceWithBuildbotConfig()
        self.assertEqual("bar", self.srvtest.returnRenderedSecrets("foo"))

    @defer.inlineCallbacks
    def test_secret_rendered_not_found(self):
        yield self.assertFailure(self.srvtest.reconfigService(secret=Secret("more")), KeyError)

    @defer.inlineCallbacks
    def test_secret_render_no_secretkey(self):
        yield self.srvtest.reconfigService(secret=Secret("foo"))
        self.assertRaises(Exception, self.srvtest.returnRenderedSecrets, "more")
